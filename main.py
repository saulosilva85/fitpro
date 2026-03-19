from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.add_widget(Label(text="🏋️ FitPro", font_size=28))

        self.add_widget(Button(text="▶️ Iniciar Treino", on_press=self.start_workout))
        self.add_widget(Button(text="📋 Meus Treinos", on_press=self.show_workouts))
        self.add_widget(Button(text="📊 Evolução", on_press=self.show_progress))

        self.status = Label(text="Bem-vindo!", font_size=16)
        self.add_widget(self.status)

    def start_workout(self, instance):
        self.status.text = "Treino iniciado!"

    def show_workouts(self, instance):
        self.status.text = "Lista de treinos (em construção)"

    def show_progress(self, instance):
        self.status.text = "Gráficos (em construção)"


class FitApp(App):
    def build(self):
        return HomeScreen()


if __name__ == "__main__":
    FitApp().run()