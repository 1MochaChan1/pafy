import pafy
import vlc
import time

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel

from yt_mod import search_con

kv = Builder.load_string("""
<MyScreen>:
    #progress:progress
    MDRectangleFlatButton:
        text:"Play"
        pos_hint:{'center_x':0.5, 'center_y':0.2}
        on_release:root.init_player()

    MDRectangleFlatButton:
        text:"Pause"
        pos_hint:{'center_x':0.6, 'center_y':0.2}
        on_release:root.pause()

    MDRectangleFlatButton:
        text:"Stop"
        pos_hint:{'center_x':0.4, 'center_y':0.2}
        on_release:root.stop()
    
""")

class MyScreen(Screen):
    progress = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        href = "https://www.youtube.com/watch?v=1K1yNqmySnA"
        #"https://www.youtube.com/watch?v=KnDVu-PLZh8", "https://www.youtube.com/watch?v=YlVdM9RLZFk"
        pafy_ins = pafy.new("https://www.youtube.com/watch?v=1K1yNqmySnA")
        self.vlc_ins = vlc.Instance()

        best = pafy_ins.getbestaudio().url

        media = self.vlc_ins.media_new(best)
        self.player = self.vlc_ins.media_player_new()
        self.player.set_media(media)

        #Getting duration
        self.duration = 61
        print(self.player.get_length())


        #print(round(self.length, 2)) #Rounding the minutes to two decimal places

        self.slider = MDSlider(
            min=0,
            max=self.duration,
            pos_hint={'center_x':0.5, 'center_y':0.35},
            size_hint=(0.4, None),
            #hint=False
        )
        self.add_widget(self.slider)
        #self.slider.bind(on_touch_up=self.set_pos)
        self.updater = None #If you want to use this as none move it to init_player() method
        
    
    #Playing the audio
    def init_player(self):
        if self.updater==None:
            self.updater = Clock.schedule_interval(self.slider_updater, 0.5)
        if self.player.is_playing():
            self.player.play()
        elif not self.player.is_playing():
            self.player.play()

        
            
    def slider_updater(self, dt):
        print(self.player.get_time()/1000)
        #self.slider.value=(self.player.get_time()/1000)
        pass
        

    def set_pos(self, obj, obj_prop):
        return obj.value

    #Stoping the audio
    def stop(self):
        if self.player.is_playing():
            self.player.stop()
            Clock.unschedule(self.updater)
        #elif not self.player.is_playing():
            #self.player.stop()
            #Clock.unschedule(self.updater)

            
    #Pausing the audio
    def pause(self):
        if self.player.is_playing():
            self.player.pause()

    

class MyApp(MDApp):
    def build(self):
        return MyScreen()

if __name__=="__main__":
    MyApp().run()