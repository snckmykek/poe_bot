from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy_garden.draggable import KXDraggableBehavior, KXReorderableBehavior
import asynckivy as ak
from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.app import MDApp

from db_requests import db
from rep_act_element_form import RepActElementForm


class Magnet(Factory.Widget):
    '''
    Inspired by
    https://github.com/kivy-garden/garden.magnet
    '''
    do_anim = BooleanProperty(True)
    anim_duration = NumericProperty(1)
    anim_transition = StringProperty('out_quad')

    # default value of the instance attributes
    _coro = ak.sleep_forever()

    def __init__(self, **kwargs):
        self._anim_trigger = trigger = \
            Clock.create_trigger(self._start_anim, -1)
        super().__init__(**kwargs)
        self.fbind('pos', trigger)
        self.fbind('size', trigger)

    def add_widget(self, widget, *args, **kwargs):
        if self.children:
            raise ValueError('Magnet can have only one child')
        widget.pos = self.pos
        widget.size = self.size
        return super().add_widget(widget, *args, **kwargs)

    def _start_anim(self, *args):
        if self.children:
            child = self.children[0]
            self._coro.close()
            if not self.do_anim:
                child.pos = self.pos
                child.size = self.size
                return
            self._coro = ak.start(ak.animate(
                child,
                d=self.anim_duration,
                t=self.anim_transition,
                x=self.x, y=self.y, width=self.width, height=self.height,
            ))


Builder.load_string("""
#:import create_spacer kivy_garden.draggable._utils._create_spacer
<Algorithm>:
    padding: dp(20)
    spacing: dp(20)
    orientation: "vertical"

    MDBoxLayout:
        spacing: dp(10)

        MDBoxLayout:
            size_hint_x: .7
            spacing: dp(20)
            orientation: "vertical"
        
            ScrollView:
                
                ReorderableGridLayout:
                    id: algorithm_actions
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: 10
                    drag_classes: ['algorithm_actions', ]
                    cols: 1
                    
            MDRectangleFlatButton:
                text: "Добавить действие"
        
        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: .3
            
            MDList:
                id: repetitive_actions
                
            Widget:
            
            MDBoxLayout:
                adaptive_height: True
                
                Widget:

                MDRectangleFlatButton:
                    text: "Добавить"
                    on_release: root.add_new_rep_act()
            

    MDBoxLayout:
        adaptive_height: True
        spacing: dp(20)
 
        Widget:
        
        MDRectangleFlatButton:
            text: "Начать" if not app.is_active else "Пауза"
            on_release: root.change_activity()
        
        MDRectangleFlatButton:
            text: "Остановить"
            on_release: root.stop()
        
                  
<ActionRow>:
    do_anim: not self.is_being_dragged
    anim_duration: .2
    drag_cls: 'algorithm_actions'
    drag_timeout: 50
    size_hint_y: None
    height: dp(50)
    opacity: .7 if self.is_being_dragged else 1.
    canvas.after:
        Color:
            rgba: [*app.theme_cls.primary_color[:3], .3 if root.is_being_dragged else .2]
        Line:
            width: 2 if root.is_being_dragged else 1
            rectangle: [*self.pos, *self.size, ]
            
    OneLineIconListItem:
        text: root.text
        
        IconLeftWidget:
            icon: "play"
            theme_text_color: "Custom"
            text_color: self.theme_cls.accent_color if root.active else (1, 1, 1, 1)
            user_font_size: 0
            on_release: root.start_stop(self)
            
            
<ReorderableGridLayout>:
    # spacer_widgets:
    #     [create_spacer(color=color)
    #     for color in "#000044 #002200 #440000".split()]
    
    
<RepAct>:
    text: root.key
        
    LeftCheckbox:
    
    IconRightWidget:
        icon: "close"
        user_font_size: dp(15)
        pos_hint: {'center_y': .5}


<LeftCheckbox@ILeftBodyTouch+MDCheckbox>:
      
""")


class ReorderableGridLayout(KXReorderableBehavior, GridLayout):
    def __init__(self, **kwargs):
        super(ReorderableGridLayout, self).__init__(**kwargs)


class ActionRow(KXDraggableBehavior, Magnet):
    text = StringProperty("")
    active = BooleanProperty(False)
    func_start_stop = ObjectProperty()

    def __init__(self, **kwargs):
        try:
            self.text = kwargs["text"]
        except KeyError:
            pass
        super(ActionRow, self).__init__()

    def start_stop(self, obj, *args):
        self.active = not self.active

        if self.func_start_stop:
            self.func_start_stop()


class Algorithm(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)

        Clock.schedule_once(lambda *x: self.load_algorithm())

    def load_algorithm(self):
        algorithm_actions = self.ids.algorithm_actions
        for i in range(23):
            algorithm_actions.add_widget(ActionRow(text=str(i)))

        self.refresh_rep_acts()

    @staticmethod
    def change_activity():
        app = MDApp.get_running_app()
        app.is_active = not app.is_active

    def stop(self):
        # Смена is_active и сбрасывание прогресса выполнения к первому шагу
        app = MDApp.get_running_app()
        if app.is_active:
            app.is_active = False
            self.reset()

    def reset(self):
        # Сбрасывание прогресса выполнения к первому шагу
        pass

    def add_action(self):
        pass

    def add_new_rep_act(self):
        rep_act_form = RepActElementForm()
        rep_act_form.key = None
        rep_act_form.open()
        pass

    def refresh_rep_acts(self):
        self.ids.repetitive_actions.clear_widgets()

        for rep_act in db.get_rep_acts():
            self.ids.repetitive_actions.add_widget(RepAct(
                key=rep_act['key'],
                name=rep_act['name'],
                frequency=rep_act['frequency'],
                active=rep_act['active']
                )
            )


class RepAct(OneLineAvatarIconListItem):
    key = StringProperty("")
    name = StringProperty("")
    frequency = NumericProperty(0)
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        # for key, val in kwargs.items():
        #     self.__dict__[key] = val

        self.key = kwargs['key']
        self.name = kwargs['name']
        self.frequency = kwargs['frequency']
        self.active = kwargs['active']

        super(RepAct, self).__init__()


