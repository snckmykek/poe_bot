from kivy.lang import Builder
from kivy.uix.modalview import ModalView

from kivymd.uix.list import OneLineListItem

from db_requests import db

Builder.load_string("""
<MapChanger>:
    size_hint: .5, .8
    padding: dp(20)
    
    MDBoxLayout:
        orientation: "vertical"
        
        ScrollView:
    
            MDList:
                id: container
                
        MDBoxLayout:
        
            MDTextField:
                id: new_map_name
                hint_text: "Имя новой карты (алгоритма)"
        
            MDRectangleFlatButton:
                text: "Добавить"
                on_release: root.add_map()
    
""")


class MapChanger(ModalView):

    def __init__(self, **kwargs):
        super(MapChanger, self).__init__(**kwargs)

    def on_pre_open(self):
        self.refresh_list()

    def refresh_list(self):
        self.ids.container.clear_widgets()
        for map_name in db.get_maps():
            self.ids.container.add_widget(
                OneLineListItem(text=str(map_name),
                                on_release=lambda *x: self.change_current_location(str(map_name)))
            )

    def change_current_location(self, location):
        self.app.set_current_location(location)
        self.dismiss()

    def add_map(self):
        db.add_map(self.ids.new_map_name.text)
        self.refresh_list()

