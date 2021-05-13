import pafy
import vlc
import time

link = pafy.new("https://www.youtube.com/watch?v=YlVdM9RLZFk")
best_audio = link.getbestaudio().url

vlc_instance = vlc.Instance()
media = vlc_instance.media_new(best_audio)
player = vlc_instance.media_player_new()
player.set_media(media)

player.play()
time.sleep(60)
