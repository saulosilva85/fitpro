import requests
from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDTextField:
            id: email
            hint_text: "Email"

        MDTextField:
            id: senha
            hint_text: "Senha"
            password: True

        MDRaisedButton:
            text: "Login"
            on_release: app.login()
'''

class AppFit(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def login(self):
        email = self.root.ids.email.text
        senha = self.root.ids.senha.text

        res = requests.post("http://127.0.0.1:8000/login",
                            params={"email": email, "senha": senha})

        print(res.json())

AppFit().run()