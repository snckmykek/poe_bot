from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '640')

from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase

from db_requests import db


class MainScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class Tab(MDBoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class MainApp(MDApp):
    current_map = StringProperty("")
    status = StringProperty("Остановлен")
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.load_settings()
        super(MainApp, self).__init__(**kwargs)

    def load_settings(self):
        self.current_map = db.get_setting("current_map")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return MainScreen()

    def set_current_location(self, current_location):
        self.current_map = current_location
        self.status = "Остановлен"
        db.set_setting("current_map", self.current_map)

    def change_status(self, new_status):
        self.status = new_status


if __name__ == "__main__":
    MainApp().run()
