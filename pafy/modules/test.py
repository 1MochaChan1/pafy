from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:

    MDRectangleFlatButton:
        text: 'Goto settings'
        on_press: root.manager.current = 'settings'
        pos_hint:{'center_x':0.5,'center_y':0.5}
    MDRectangleFlatButton:
        text: 'More'
        pos_hint:{'center_x':0.5,'center_y':0.4}
        on_release:root.add_btn()

<SettingsScreen>:
    MDRectangleFlatButton:
        text: 'My settings button'
        pos_hint:{'center_x':0.5,'center_y':0.5}
    MDRectangleFlatButton:        
        text: 'Back to menu'
        pos_hint:{'center_x':0.5,'center_y':0.4}
        on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    def add_btn(self):
        self.btn = MDRectangleFlatButton(
            text='New Button',
            pos_hint={'center_x':0.5, 'center_y':0.3},
            )
        self.btn.bind(on_release=lambda x:sm.r )
        self.add_widget(self.btn)

class SettingsScreen(Screen):
    pass

sm = ScreenManager()

class TestApp(MDApp):

    def build(self):
        # Create the screen manager
        
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()