from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField

import sqlite3

KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    HomeScreen:
    WorkoutScreen:

<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        padding: 30
        spacing: 25

        MDLabel:
            text: "Login"
            halign: "center"
            font_style: "H4"

        MDTextField:
            id: email
            hint_text: "Email"

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "56dp"

            MDTextField:
                id: senha
                hint_text: "Senha"
                password: True

            MDIconButton:
                id: eye_login
                icon: "eye-off"
                pos_hint: {"center_y": 0.5}
                on_release: app.toggle_password("login")

        MDRaisedButton:
            text: "Entrar"
            on_release: app.login(email.text, senha.text)

        MDFlatButton:
            text: "Criar conta"
            on_release: app.root.current = "register"


<RegisterScreen>:
    name: "register"

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: 30
            spacing: 25
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "Cadastro"
                halign: "center"
                font_style: "H4"

            MDTextField:
                id: nome
                hint_text: "Nome"

            MDTextField:
                id: email
                hint_text: "Email"

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: "56dp"

                MDTextField:
                    id: senha
                    hint_text: "Senha"
                    password: True

                MDIconButton:
                    id: eye_register
                    icon: "eye-off"
                    pos_hint: {"center_y": 0.5}
                    on_release: app.toggle_password("register")

            MDTextField:
                id: peso
                hint_text: "Peso (kg)"

            MDTextField:
                id: objetivo
                hint_text: "Objetivo (ex: hipertrofia)"

            MDRaisedButton:
                text: "Cadastrar"
                on_release: app.registrar(nome.text, email.text, senha.text, peso.text, objetivo.text)

            MDFlatButton:
                text: "Voltar"
                on_release: app.root.current = "login"


<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "FitPro"
            right_action_items: [["logout", lambda x: app.logout()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 20

            MDRaisedButton:
                text: "Iniciar Treino"
                on_release: app.ir_treino()


<WorkoutScreen>:
    name: "workout"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Treino"
            left_action_items: [["arrow-left", lambda x: app.voltar()]]

        ScrollView:
            MDBoxLayout:
                id: lista_exercicios
                orientation: "vertical"
                padding: 10
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

        MDFloatingActionButton:
            icon: "plus"
            pos_hint: {"right": 0.95, "y": 0.05}
            on_release: app.abrir_dialog()
'''


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class WorkoutScreen(Screen):
    pass


class FitApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.conn = sqlite3.connect("fitpro.db")
        self.criar_tabelas()

        return Builder.load_string(KV)

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            senha TEXT,
            peso TEXT,
            objetivo TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            series TEXT,
            reps TEXT,
            peso TEXT
        )
        """)

        self.conn.commit()

    # 🔥 CORRIGIDO
    def toggle_password(self, tela):
        if tela == "login":
            screen = self.root.get_screen("login")
            campo = screen.ids.senha
            icon = screen.ids.eye_login
        else:
            screen = self.root.get_screen("register")
            campo = screen.ids.senha
            icon = screen.ids.eye_register

        campo.password = not campo.password
        icon.icon = "eye" if not campo.password else "eye-off"

    def login(self, email, senha):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        user = cursor.fetchone()

        if user:
            self.root.current = "home"

            tela = self.root.get_screen("login")
            tela.ids.email.text = ""
            tela.ids.senha.text = ""

    def registrar(self, nome, email, senha, peso, objetivo):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, peso, objetivo) VALUES (?, ?, ?, ?, ?)",
            (nome, email, senha, peso, objetivo)
        )
        self.conn.commit()

        tela = self.root.get_screen("register")
        tela.ids.nome.text = ""
        tela.ids.email.text = ""
        tela.ids.senha.text = ""
        tela.ids.peso.text = ""
        tela.ids.objetivo.text = ""

        self.root.current = "login"

    def logout(self):
        self.root.current = "login"

    def ir_treino(self):
        self.root.current = "workout"
        self.atualizar_lista()

    def voltar(self):
        self.root.current = "home"

    def salvar_exercicio(self, nome, series, reps, peso):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO exercicios (nome, series, reps, peso) VALUES (?, ?, ?, ?)",
            (nome, series, reps, peso)
        )
        self.conn.commit()

    def carregar_exercicios(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, series, reps, peso FROM exercicios")
        return cursor.fetchall()

    def deletar_exercicio(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM exercicios WHERE id=?", (id,))
        self.conn.commit()

    def atualizar_lista(self):
        lista = self.root.get_screen("workout").ids.lista_exercicios
        lista.clear_widgets()

        for id, nome, series, reps, peso in self.carregar_exercicios():
            card = MDCard(size_hint=(1, None), height=120, padding=15)

            layout = Builder.load_string(f'''
BoxLayout:
    orientation: "vertical"

    Label:
        text: "{nome}"
    Label:
        text: "{series}x{reps} - {peso}kg"
''')

            btn = MDRaisedButton(text="Excluir", on_release=lambda x, i=id: self.remover(i))

            card.add_widget(layout)
            card.add_widget(btn)

            lista.add_widget(card)

    def remover(self, id):
        self.deletar_exercicio(id)
        self.atualizar_lista()

    def abrir_dialog(self):
        self.nome = MDTextField(hint_text="Ex: Supino")
        self.series = MDTextField(hint_text="Séries")
        self.reps = MDTextField(hint_text="Reps")
        self.peso = MDTextField(hint_text="Peso")

        layout = Builder.load_string('''
BoxLayout:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: "250dp"
''')

        layout.add_widget(self.nome)
        layout.add_widget(self.series)
        layout.add_widget(self.reps)
        layout.add_widget(self.peso)

        self.dialog = MDDialog(
            title="Novo Exercício",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Salvar", on_release=lambda x: self.salvar_dialog())
            ]
        )
        self.dialog.open()

    def salvar_dialog(self):
        if self.nome.text:
            self.salvar_exercicio(self.nome.text, self.series.text, self.reps.text, self.peso.text)
            self.dialog.dismiss()
            self.atualizar_lista()


if __name__ == "__main__":
    FitApp().run()