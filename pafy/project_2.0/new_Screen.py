from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

import time

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.label import MDLabel

screen_helper = """
ScreenManager:
    MenuScreen:
    SettingsScreen:
    OngaBunga:
    


<MenuScreen>:
    name:'menu'
    MDRectangleFlatButton:        
        text: 'Profile'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_release:root.add_btn()
        
    MDRectangleFlatButton:        
        text: 'Profile'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_release:root.manager.current = 'onga


<SettingsScreen>:
    name:'settings'
    MDLabel:        
        text: 'This is Settings Screen'
        halign:'center'
        
        
    MDRectangleFlatButton:
        text: 'Go Back'
        pos_hint: {'center_x':0.5,'center_y':0.4}
        on_release:root.manager.current='menu'

<OngaBunga>:
    name:'onga'
    MDRectangleFlatButton:        
        text: 'Profile'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_release:root.add_btn()


"""


class MenuScreen(Screen):
    #menuscreen = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MenuScreen,self).__init__(**kwargs)

    def add_btn(self):
        self.btn = MDRectangleFlatButton(
            text='New Button',
            pos_hint={'center_x':0.5, 'center_y':0.4},
            )
        self.btn.bind(on_release=lambda x:sm.switch_to(SettingsScreen(name='settings')) )
        self.add_widget(self.btn)
        
        
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

class OngaBunga(Screen):
    def __init__(self, **kwargs):
        super(OngaBunga, self).__init__(**kwargs)


sm = ScreenManager()


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper) 
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(OngaBunga(name='onga'))
        return sm #returning the screen manager lets the switch_to() method work


DemoApp().run()