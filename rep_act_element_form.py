from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty

from kivymd.app import MDApp

from db_requests import db

Builder.load_string("""
<RepActElementForm>:
    size_hint: .5, .8
    padding: dp(20)
    
    MDBoxLayout:
        orientation: 'vertical'
    
        MDLabel:
            adaptive_size: True
            text: "Повторяющееся действие"
        Widget:
            size_hint_y: None
            height: dp(15)
                
        MDStackLayout:
            # adaptive_height: True
    
            MDTextField:
                id: new_key
                hint_text: "Уникальный ключ действия"
    
            MDTextField:
                id: new_name
                hint_text: "Имя действия"
    
            MDTextField:
                id: new_frequency
                hint_text: "Частота в секундах (десятые - через точку)"
    
            ScrollView:
                size_hint_y: None
                height: dp(250)
                
                MDTextField:
                    id: new_script
                    multiline: True
                    hint_text: "Скрипт"
    
        MDRectangleFlatButton:
            text: "Сохранить"
            on_release: root.add_map()

""")


class RepActElementForm(ModalView):
    key = ObjectProperty()
    name = StringProperty("")
    frequency = NumericProperty(0)
    script = StringProperty("")

    def __init__(self, **kwargs):
        super(RepActElementForm, self).__init__(**kwargs)

    def on_pre_open(self):

        if self.key:
            rep_act = db.get_rep_act(self.key)
            self.name = rep_act['name']
            self.frequency = rep_act['frequency']
            self.script = rep_act['script']
