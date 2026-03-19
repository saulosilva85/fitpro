from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

import sqlite3

KV = '''
ScreenManager:
    HomeScreen:
    WorkoutScreen:

<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDLabel:
            text: "🏋️ FitPro"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Iniciar Treino"
            pos_hint: {"center_x": 0.5}
            on_release: app.ir_treino()

        MDRaisedButton:
            text: "Sair"
            pos_hint: {"center_x": 0.5}
            on_release: app.stop()

<WorkoutScreen>:
    name: "workout"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Treino"
            left_action_items: [["arrow-left", lambda x: app.voltar()]]

        ScrollView:
            MDList:
                id: exercise_list

        MDRaisedButton:
            text: "Adicionar Exercício"
            pos_hint: {"center_x": 0.5}
            on_release: app.abrir_dialog()
'''

class HomeScreen(Screen):
    pass

class WorkoutScreen(Screen):
    pass


class FitApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.conn = sqlite3.connect("treinos.db")
        self.criar_tabela()

        return Builder.load_string(KV)

    # ================= BANCO =================
    def criar_tabela(self):
        cursor = self.conn.cursor()
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

    def salvar_exercicio(self, nome, series, reps, peso):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO exercicios (nome, series, reps, peso) VALUES (?, ?, ?, ?)",
                       (nome, series, reps, peso))
        self.conn.commit()

    def carregar_exercicios(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nome, series, reps, peso FROM exercicios")
        return cursor.fetchall()

    # ================= NAVEGAÇÃO =================
    def ir_treino(self):
        self.root.current = "workout"
        self.atualizar_lista()

    def voltar(self):
        self.root.current = "home"

    # ================= LISTA =================
    def atualizar_lista(self):
        lista = self.root.get_screen("workout").ids.exercise_list
        lista.clear_widgets()

        for nome, series, reps, peso in self.carregar_exercicios():
            item = TwoLineListItem(
                text=f"{nome}",
                secondary_text=f"{series}x{reps} - {peso}kg"
            )
            lista.add_widget(item)

    # ================= DIALOG =================
    def abrir_dialog(self):
        self.nome = MDTextField(hint_text="Nome do exercício")
        self.series = MDTextField(hint_text="Séries (ex: 3)")
        self.reps = MDTextField(hint_text="Repetições (ex: 10)")
        self.peso = MDTextField(hint_text="Peso (kg)")

        layout = Builder.load_string('''
BoxLayout:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: "200dp"
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
        nome = self.nome.text
        series = self.series.text
        reps = self.reps.text
        peso = self.peso.text

        if nome:
            self.salvar_exercicio(nome, series, reps, peso)
            self.dialog.dismiss()
            self.atualizar_lista()


if __name__ == "__main__":
    FitApp().run()