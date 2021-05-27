from kivymd.uix import label
import pafy
import vlc
import time

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel


kv = Builder.load_string("""
<MyScreen>:
    search:search
    MDTextField:
        id:search
        size_hint:(0.4, None)
        pos_hint:{'center_x':0.5,'center_y':0.85}

    MDIconButton:
        icon:'magnify'
        pos_hint:{'center_x':0.7, 'center_y':0.85}
        on_release:root.search_()

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
    global player, media
    search = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Objecto property for the search bar
        

        #Getting duration       
        self.duration = 60.9 #duration of the video
        
        #Creating elapsed time label
        self.elapsed = MDLabel(
            text="00:00:00",
            halign='center'
        )

        #Creating the slider
        self.slider = MDSlider(
            min=0,
            max=self.duration,
            pos_hint={'center_x':0.5, 'center_y':0.35},
            size_hint=(0.4, None),
        )

        #Fires the function callback in MySlider class
        #self.set_time = self.slider.on_touch_up
        self.slider.bind(on_touch_up = self.content_update)
        self.add_widget(self.elapsed)
        self.add_widget(self.slider)

        self.slider.value = 0        
        self.updater = None

    #Search
    def search_(self):
        if player.is_playing():
            dialog = MDDialog(
                text="First stop the current player please"
            )
            dialog.open()
        else:
            init_vlc(self.search.text)

    #Playing the audio
    def init_player(self):
        self.updater = None

        if self.updater == None:
            self.updater = Clock.schedule_interval(self.slider_updater, 1) #Cla

        if player.is_playing():
            player.play()
        elif not player.is_playing():
            player.play()
        
    #Incrementing the value of slider every second                
    def slider_updater(self, dt):

        #Converting seconds into time format
        elapsed = player.get_time()/1000 # elapsed is in seconds
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed)) # elapsed_time is in time format
        
        #Displaying elapsed time
        self.elapsed.text = str(elapsed_time)
        self.slider.value=(player.get_time()/1000)

        if elapsed >= (self.duration-5) and player.is_playing() == 0:
            self.stop()

    #Traversing through the content's timeline
    def content_update(self, slider, touch):
        if slider.collide_point(*touch.pos):
            player.set_time(int(slider.value*1000))
        
    #Stoping the audio
    def stop(self):
        #When the player is still playing the audio
        if player.is_playing():
            player.stop()
            self.slider.value = 0
            self.elapsed.text = str("00:00:00")

        #When the player is finished playing the audio
        elif not player.is_playing():
            player.stop()
            self.slider.value = 0
            self.elapsed.text = str("00:00:00")
        Clock.unschedule(self.updater)

    #Pausing the audio
    def pause(self):
        if player.is_playing():
            player.pause()
        Clock.unschedule(self.updater)

class MyApp(MDApp):
    def build(self):
        return MyScreen()

def init_vlc(content):
    global player, media
    pafy_ins = pafy.new(content)
    vlc_ins = vlc.Instance()

    best = pafy_ins.getbestaudio().url
    media = vlc_ins.media_new(best)
    player = vlc_ins.media_player_new()
    player.set_media(media)

if __name__=="__main__":
    init_vlc("https://www.youtube.com/watch?v=1K1yNqmySnA")
    MyApp().run()
