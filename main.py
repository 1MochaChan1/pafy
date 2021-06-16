from kivy.uix.boxlayout import BoxLayout
import pafy
import time
import vlc
import sys
import threading

from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.actionbar import ActionBar, ActionBarException, ActionButton, ActionItem
from kivy.properties import ObjectProperty, StringProperty


from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

from yt_mod_1 import search_content

#============Storing Selected Video's Details Using Global Var==========#
video_thumbnail = ''
video_title = ''
video_link = ''
video_duration=''

is_playing_now = False
media_set = False
#============== Setting Media To Player ===============#
def set_media(content_url):
    global media, player, media_set
    pafy_inst = pafy.new(content_url) #Creates pafy instance
    Instance = vlc.Instance() #Creates vlc instance

    best = pafy_inst.getbestaudio().url #Gets best link for bestaudio
    
    media = Instance.media_new(best) #Creates new media to be played by a MeidaPlayer
    player = Instance.media_player_new() #Creating a MediaPlayer instance
    player.set_media(media) #Setting the media in the player to be played
    media_set = True #Making flag to check if the player has some media in it

#=================== Search Screen ==================#
class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class BuildScreen(Screen):
    def __init__(self, **kwargs):
        super(BuildScreen, self).__init__(**kwargs)

    #Fetching the id of GridLayout from test.kv
        self.container = self.ids.container
        self.sleep_time = [10, 15, 20, 30, 40, 60]
        menu_items=[
            {   "viewclass": "IconListItem",
                "icon": "git",
                "height": dp(56),
                "text":f'{i}min',
                'on_release': lambda x=i : self.sleep(x)
            }for i in self.sleep_time
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,

        )
    
    #Opens the timer menu in the bottom left
    def open_menu(self, btn):
        self.menu.caller = btn
        self.menu.open()
        
    #Sets the sleep timer and once time's up the program terminates
    def sleep(self, sleep_in):
        print("success")
        stop_program = lambda : MDApp.get_running_app().stop()
        timer = threading.Timer(sleep_in*60, stop_program)
        timer.start()

    #To check if the player is playing while user is in search screen
    def on_enter(self):
        self.playing = is_playing_now
        self.set = media_set

    #Searching for a Video
    def search(self):
        for child in self.container.children[:]: #Removes the widget enlisted. (Refreshes)
            self.container.remove_widget(child)

        self.query = self.ids.search.text #Fetching query term
        if self.query == "": #Checking if the search is empty
            dialog = "The Search Box is Empty"
            title = "Error"
            close_btn = MDRectangleFlatButton(text="Close", on_release=self.close_dial)
            self.dial = MDDialog(
                title= title,
                text = dialog,
                buttons=[close_btn]
            )
            self.dial.open() #Opening a Dialog Box
        
        #Running the Search module
        results = search_content(self.query)
           
        for k,v in results.items():

            #Fetching the title, thumbnail, link and length of the video
            title = v[0]
            if len(title)>40:
                title = title[:35] + '...'
            thumbnail=v[1]
            link = v[2]
            duration = v[3]
            
            #Convertin the duration of the video from sec to time format
            length = time.strftime("%H:%M:%S", time.gmtime(int(duration)))
            
            #The Layout above the MDSeparator
            self.screen = MDGridLayout(
                cols=2,
                size_hint=(.95, 1),
                pos_hint={'center_x':0.45},
            )

            #The Layout Below the MDSeparator
            self.screen_2 = MDBoxLayout(
                orientation='horizontal',
                pos_hint={'center_x':0.8},
                size_hint=(0.6,0.3),          
            )

            #Video Title
            vid_title = MDLabel(
                text=title,
                size_hint = (1,1),
                padding=(10,0)
            )

            #Video Link
            vid_link_dur = MDLabel(
                text=f"{link},{str(duration)}",
                size_hint = (None, None),
                size = (dp(0), dp(0))
            )

            #Video Thumbnail
            vid_thumb=AsyncImage(
                source=thumbnail,
                size_hint=(1, 1),
            )
            #Video Card
            card = MDCard(
                orientation='vertical',
                size_hint=(1,None),
                pos_hint={'center_x':0.5},
                focus_behavior=True,
                ripple_behavior=True
            )
    
            separator = MDSeparator(
                height=dp(1)
            )

            #Length Label
            length_label = MDLabel(
                text=f'Length :{length} ',
                pos_hint={'center_x':1},
                padding=(10,0)
            )


            #Binding function to the card 
            card.bind(on_release = self.get_video)
            
            #Adding elements to first layout
            self.screen.add_widget(vid_thumb)
            self.screen.add_widget(vid_title)
            self.screen.add_widget(vid_link_dur) #Hidden link and duration
            
            #Adding elements to second layout
            self.screen_2.add_widget(length_label)
            #self.screen_2.add_widget(video_length)


            #Adding everything to the Video Card
            card.add_widget(self.screen)
            card.add_widget(MDSeparator(height = dp(1)))
            card.add_widget(self.screen_2)
            
            #Adding Video Card to the created GridLayout
            self.container.add_widget(card)


    #Dialog Box for error    
    def close_dial(self, obj):
        self.dial.dismiss()

    #Gets the thumbnail and title of the selected link.
    def get_video(self,obj):
        global video_link, video_thumbnail, video_title, video_duration

        for layout in obj.children[:]:
            for child in layout.children[:]:
                if isinstance(child, AsyncImage):
                    video_thumbnail = child.source

                if isinstance(child, MDLabel) and child.text.startswith("https://"):
                    link_dur = child.text.split(",")
                    video_link = link_dur[0]
                    video_duration = float(link_dur[1])
                    

                elif isinstance(child, MDLabel):
                    video_title=child.text
        self.change_screen()

    def change_screen(self):                    
        self.parent.current = "player" #sm.switch_to(PlayerScreen(name='player'))

#================= Player Screen =================#
class PlayerScreen(Screen):    
    
    elapsed = ObjectProperty(None)
    play_btn = ObjectProperty(None)
    img = ObjectProperty(None)
    title = ObjectProperty(None)
    slide = ObjectProperty(None)
    length=ObjectProperty(None)

    def __init__(self, **kw):                
        super(PlayerScreen, self).__init__(**kw)
        global video_link, video_thumbnail, video_title, video_duration, is_playing_now
        
        #Slider Flag
        self.slider_exists = False

    def on_enter(self):   
   
        #Duration of the audio
        self.duration = video_duration
        self.length.text = time.strftime("%H:%M:%S", time.gmtime(int(self.duration)))

        #Adding and updater variable
        self.updater = None
        
        if is_playing_now == False or is_playing_now == True and self.link != video_link :
            if self.slider_exists == True:
                self.remove_widget(self.slider)
                self.slider_exists == False
            self.add_elements()
        

    def add_elements(self):
        self.link = video_link

        if is_playing_now == False:
            set_media(self.link)
            self.play()
        elif is_playing_now == True:
            player.stop()
            set_media(self.link)
            self.play()

        #Setting the thumb and title of the selected video
        self.img.source  = video_thumbnail
        self.title.text = video_title

        #Creating Slider
        self.slider = MDSlider(
            min=0,
            max=self.duration,
            pos_hint={'center_x':0.5, 'center_y':0.3},
            size_hint=(.5, 0.02)
        )
        self.slider.bind(on_touch_up = self.set_slider)

        #Adding all the elements to the screen:
        #Slider and Elements
        self.add_widget(self.slider)
        self.slider_exists = True

    #Playing the custom Player
    def play(self):
        global player, media , is_playing_now       
        if self.updater == None:
            self.updater = Clock.schedule_interval(self.update_slider, 1)

        if player.is_playing():
            player.pause()
            is_playing_now = False
            self.play_btn.icon = "play"

        elif not player.is_playing():
            player.play()
            is_playing_now = True
            self.play_btn.icon = "pause"

    def update_slider(self, clock):
        elapsed = player.get_time()/1000

        self.elapsed.text = time.strftime("%H:%M:%S", time.gmtime(int(player.get_time()/1000)))
        self.slider.value = elapsed

        if elapsed >= (self.duration-4) and player.is_playing() == 0:
            player.stop()
            
    def set_slider(self,slider, touch):
        if slider.collide_point(*touch.pos):
            player.set_time(int(slider.value*1000))
         

    #Goes back to search
    def go_back(self):
        self.parent.current = "search" #sm.switch_to(BuildScreen(name='search'))

        

sm = ScreenManager()

class DemoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm.add_widget(BuildScreen(name='search'))
        sm.add_widget(PlayerScreen(name='player'))
        return sm

        
if __name__ == "__main__":
    DemoApp().run()
