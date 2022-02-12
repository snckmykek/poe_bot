from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy_garden.draggable import KXDraggableBehavior, KXReorderableBehavior
import asynckivy as ak
from kivymd.uix.list import OneLineAvatarListItem


from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

from db_requests import db


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

        ScrollView:
            
            ReorderableGridLayout:
                id: algorithm_actions
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
                padding: 10
                drag_classes: ['algorithm_actions', ]
                cols: 1

    MDBoxLayout:
        adaptive_height: True
        padding: dp(20), 0
        spacing: dp(20)
        
        MDRectangleFlatButton:
            text: "Добавить действие"
            on_release: root.change_activity()
        
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




