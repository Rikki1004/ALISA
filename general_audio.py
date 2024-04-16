import time, threading
import vlc
import vk_audio, yandex_audio

service = vk_audio
is_moya_musica = False

media_player = vlc.MediaPlayer()  # vlc.MediaListPlayer()
media_player.audio_set_mute(False)
player = vlc.Instance()
event_manager = media_player.event_manager()
cur_volume = media_player.audio_get_volume()

def whats_playing_now():
    if (len(trackHistory) > 0):
        return f"{trackHistory[-1]['artist']} - {trackHistory[-1]['title']}"
    else:
        return "Сейчас ничего не играет"


def on_end_reached(event_data):
    print("End of media reached")
    threading.Thread(target=next_track).start()

event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_end_reached)

curTrackList = []
trackHistory = []
mute_status = False


def play_sound(artist, title):
    global is_moya_musica
    is_moya_musica = False

    curTrackList.clear()
    query = "черный бумер"
    if (artist and title):
        query = f"{artist} - {title}"
    elif (not artist and title == "my"):
        is_moya_musica = True
        service.moya_musica_offset = 0
        service.moya_musica(curTrackList, next_track)
        return
    elif (not artist and title == "volna"):
        next_track()
        return
    elif (artist and not title):
        query = artist
    elif (not artist and title):
        query = title
    else:
        next_track()
        return

    service.find(curTrackList, query, next_track)


def independent_volume(volume=None):
    if (volume):
        media_player.audio_set_volume(volume)
    else:
        media_player.audio_set_volume(cur_volume)


def change_volume(volume, number=""):
    global cur_volume
    min_volume = 20
    max_volume = 100
    current_volume = cur_volume + 0  # media_player.audio_get_volume()
    if (not volume and number):
        new_volume = int(number)
    elif (volume and not number):
        new_volume = current_volume + int(volume)

    else:
        if (int(volume) >= 0):
            new_volume = int(number) * current_volume
        else:
            new_volume = int(current_volume / int(number))

    if (new_volume > min_volume):
        if (new_volume < max_volume):
            volume = new_volume
        else:
            volume = max_volume
    else:
        volume = min_volume

    print("volume to: ", volume)

    cur_volume = volume + 0
    media_player.audio_set_volume(volume)


def next_track():
    time.sleep(0.3)
    # media_player.next()
    if (len(curTrackList) == 0):
        if (is_moya_musica):
            service.moya_musica(curTrackList,next_track)
            return
        else:
            curTrackList.append(service.moya_volna(trackHistory))
        # return
    track = curTrackList.pop(0)
    print("track: ", track)
    media_player.set_media(vlc.Media(track["url"]))
    media_player.play()
    trackHistory.append(track)

    if (len(trackHistory) > 50):
        trackHistory.pop(0)


def prev_track():
    if (len(trackHistory) < 2):
        return
    prevTrack = trackHistory.pop(-1)
    prevPrevTrack = trackHistory.pop(-1)
    curTrackList.insert(0, prevTrack)
    curTrackList.insert(0, prevPrevTrack)
    next_track()

def pause(to=None):
    if (to == None):
        media_player.pause()
    elif (to == False):
        media_player.set_pause(0)
    elif (to == True):
        media_player.set_pause(1)


def mute(to=None):
    global mute_status

    if (to == None):
        mute_status = not mute_status
    elif (to == False):
        mute_status = False
    elif (to == True):
        mute_status = True

    media_player.audio_set_mute(mute_status)


def change_service(new_service):
    global service
    if new_service == "vk":
        service = vk_audio
    elif new_service == "yandex":
        service = yandex_audio

# media_player.audio_set_mute(False)
# moya_musica()
# media_player.set_media(vlc.Media("./start.mp3"))
# media_player.play()
# mute()
# play_sound("","my")
# time.sleep(9999)




