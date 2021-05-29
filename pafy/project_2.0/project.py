import pafy
import time
import vlc

from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout

from yt_mod import search_content

#====Fetching the Url=====#
url = "https://www.youtube.com/watch?v=-KfG8kH-r3Y"
audio = pafy.new(url) #Gets the data from the url

best = audio.getbest() #Gets the best video stream from the url (str)
best_url = best.url #fetches the url with the "best" video stream (link/url)

#============Storing Selected Video's Details==========#
video_thumbnail = ''
video_title = ''
video_link = ''

class BuildScreen(Screen):
    def __init__(self, **kwargs):
        super(BuildScreen, self).__init__(**kwargs)
        self.Instance = vlc.Instance() #Creates vlc instance
        self.Media = self.Instance.media_new(best_url) #Creates new media to be played by a MeidaPlayer
        self.player = self.Instance.media_player_new() #Creating a MediaPlayer instance
        self.player.set_media(self.Media) #Setting the media in the player to be played
        #self.container = sm.get_screen('search').ids.container 
        self.container = self.ids.container     #Fetching the id of GridLayout from test.kv

    #Playing the audio
    def init_player(self):
        if self.player.is_playing():
            self.player.play()
        elif not self.player.is_playing():
            self.player.play()

    #Stoping the audio
    def stop(self):
        if self.player.is_playing():
            self.player.stop()
            
    #Pausing the audio
    def pause(self):
        if self.player.is_playing():
            self.player.pause()
    
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
        

        results = search_content(self.query)

        
        try: #Listing search results, handling exceptions
            for k,v in results.items():
                title = v[0]
                if len(title)>50:
                    title = title[:50] + '...'
                thumbnail=v[1]
                link = v[2]
                
                self.screen = MDGridLayout(
                    cols=2,
                    size_hint=(.95, 1),
                    pos_hint={'center_x':0.45},
                    #spacing=(10,0)
                )
                
                vid_title = MDLabel(
                    text=title,
                    padding=(10,0)
                )
                
                vid_link = MDLabel(
                    text=link,
                    size_hint=(None, None),
                    size=(dp(0),dp(0))
                )

                vid_thumb=AsyncImage(
                    source=thumbnail,
                    size_hint=(1, None),
                    #size = self.size

                )

                card = MDCard(
                    orientation='vertical',
                    size_hint=(1,None),
                    pos_hint={'center_x':0.5},
                    focus_behavior=True,
                    ripple_behavior=True
                )
                card.bind(on_release = self.get_video)
                
                self.screen.add_widget(vid_thumb)
                self.screen.add_widget(vid_title)
                
                card.add_widget(self.screen)
            
                self.container.add_widget(card)
                self.screen.add_widget(vid_link)
                #print(f"{k}:\t{v[0]}\n\t{v[1]}\n\t{v[2]}\n")
        except:
            UnboundLocalError()

    #Dialog Box for error    
    def close_dial(self, obj):
        self.dial.dismiss()

    #Gets the thumbnail and title of the selected link.
    def get_video(self,obj):

        global video_link, video_thumbnail, video_title

        for layout in obj.children[:]:
            for child in layout.children[:]:
                if isinstance(child, AsyncImage):
                    video_thumbnail = child.source
                if isinstance(child, MDLabel):
                    if child.text.startswith("https://www.youtube.com"):
                        video_link = child.text
                    else:
                        video_title = child.text
                
        sm.switch_to(PlayerScreen(name='player'))

class PlayerScreen(Screen):
    global video_link, video_thumbnail, video_title
    def on_enter(self):
        print(video_title)
        print(video_thumbnail)
        print(video_link)

        playing = MDCard(
            orientation='vertical',
            pos_hint={'center_x':0.5, 'center_y':0.6},
            size_hint=(0.4,0.3)
        )
        playing_thumb = AsyncImage(
            source = video_thumbnail,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        playing_title = MDLabel(
            text=video_title,
            pos_hint={'center_y':0.35},
            halign='center'
        )
        playing.add_widget(playing_thumb)
        self.add_widget(playing)
        self.add_widget(playing_title)

    def __init__(self,**kwargs):        
        super().__init__(**kwargs)
        self.back = MDIconButton(
            icon='chevron-left',
            pos_hint={'center_x':0.1, 'center_y':0.85},
            on_release=self.go_back
        )
        self.add_widget(self.back)
        
    def go_back(self, obj):
        sm.switch_to(BuildScreen(name='search'))

sm = ScreenManager()

class DemoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm.add_widget(BuildScreen(name='search'))
        sm.add_widget(PlayerScreen(name='player'))
        return sm
        
if __name__ == "__main__":
    DemoApp().run()
