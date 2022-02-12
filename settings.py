from kivy.lang import Builder

from kivymd.uix.boxlayout import MDBoxLayout

from map_changer import MapChanger
from db_requests import db

Builder.load_string("""
<Settings1>:
    orientation: "vertical"
    
    MDBoxLayout:
        padding: dp(20)
        
        StackLayout:
        
            MDBoxLayout:
                adaptive_height: True
                
                MDLabel:
                    text: app.current_map
        
                MDRectangleFlatButton:
                    text: "Изменить"
                    on_release: root.change_map()
            
        Widget:
            size_hint_x: None
            width: dp(10)
        
        MDBoxLayout:
            adaptive_height: True

""")


class Settings1(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Settings1, self).__init__(**kwargs)

    def change_map(self):
        MapChanger().open()

