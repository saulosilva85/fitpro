from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

KV = '''
ScreenManager:
    HomeScreen:
    WorkoutScreen:
    ProgressScreen:

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
            on_release: app.root.current = "workout"

        MDRaisedButton:
            text: "Evolução"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "progress"

        MDRaisedButton:
            text: "Sair"
            pos_hint: {"center_x": 0.5}
            on_release: app.stop()

<WorkoutScreen>:
    name: "workout"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Treino A"
            left_action_items: [["arrow-left", lambda x: app.voltar()]]

        ScrollView:
            MDList:
                id: exercise_list

        MDRaisedButton:
            text: "Adicionar Exercício"
            pos_hint: {"center_x": 0.5}
            on_release: app.add_exercise()

<ProgressScreen>:
    name: "progress"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Evolução"
            left_action_items: [["arrow-left", lambda x: app.voltar()]]

        MDLabel:
            text: "📊 Em breve: gráficos de evolução"
            halign: "center"
'''

class HomeScreen(Screen):
    pass

class WorkoutScreen(Screen):
    pass

class ProgressScreen(Screen):
    pass


class FitApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def voltar(self):
        self.root.current = "home"

    def add_exercise(self):
        exercise_name = f"Exercício {len(self.root.get_screen('workout').ids.exercise_list.children)+1}"
        item = OneLineListItem(text=exercise_name)
        self.root.get_screen('workout').ids.exercise_list.add_widget(item)


if __name__ == "__main__":
    FitApp().run()