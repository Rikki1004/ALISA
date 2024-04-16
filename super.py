import asyncio
import nest_asyncio
import time
import warnings
import os
import threading
import general_audio
from speech_recognition import YandexVoiceRecognition
from text_to_voise import YandexVoiceGenerator
from google.cloud import dialogflow
from playsound import playsound
nest_asyncio.apply()

loop = asyncio.get_event_loop()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'
PROJECT_ID = ''
SESSION_ID = ''
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID,SESSION_ID)

tts = YandexVoiceGenerator(voice="tatyana_shitova.gpu")
warnings.simplefilter("ignore")
i_speak = False

def make_silent(duration = 4.5, from_thread=False):
    if(not from_thread):
        general_audio.independent_volume(40)
        threading.Thread(target=make_silent, args=(duration, True)).start()
    else:
        time.sleep(duration)
        if not i_speak:
            general_audio.independent_volume(None)


def speak(what):
    global i_speak
    i_speak = True
    general_audio.independent_volume(40)
    tts.voice(what)
    time.sleep(0.5)
    general_audio.independent_volume(None)
    i_speak = False


def dialog_flow_answer(text):
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session":session, "query_input": query_input}
    )
    parameter_list = {}
    for param_name, param_value in response.query_result.parameters.items():
        parameter_list[param_name] = param_value
    
    return response.query_result.fulfillment_text, response.query_result.intent.display_name, parameter_list, response.query_result.all_required_params_present


def action(text):
    print(text)
    if (1==1):
        answer = dialog_flow_answer(text)
        print("recived: ", answer)

        if (answer[3]):
            if (answer[0]):
                speak(answer[0])

            if (answer[1] == "Music start"):
                if ("song_service_name" in answer[2]):
                    if (answer[2]["song_service_name"] == "vk"):
                        general_audio.change_service("vk")
                    elif (answer[2]["song_service_name"] == "yandex"):
                        general_audio.change_service("yandex")
                general_audio.play_sound(answer[2]["music-artist"], answer[2]["song_name"])
            if (answer[1] == "Music volume"):
                general_audio.change_volume(answer[2]["volume"], answer[2]["number"])
            if (answer[1] == "Music actions"):
                if (answer[2]["song_actions"] == "?"):
                    speak(general_audio.whats_playing_now())
                elif (answer[2]["song_actions"] == ">"):
                    general_audio.next_track()
                elif (answer[2]["song_actions"] == "<"):
                    general_audio.prev_track()
                elif (answer[2]["song_actions"] == "||+"):
                    general_audio.pause(True)
                elif (answer[2]["song_actions"] == "||-"):
                    general_audio.pause(False)
                elif (answer[2]["song_actions"] == "||"):
                    general_audio.pause()
                elif (answer[2]["song_actions"] == "/+"):
                    general_audio.mute(True)
                elif (answer[2]["song_actions"] == "/-"):
                    general_audio.mute(False)
                elif (answer[2]["song_actions"] == "/"):
                    general_audio.mute()
            if (answer[1] == "Default Fallback Intent"):
                speak("Скажи еще раз")
                return
        else:
            speak(answer[0])
            # speak("Я вас не поняла")
            return
        if (answer[1] == 'smalltalk.greetings.bye'):
            print("end")
            playsound('./stop.mp3')


def i_listen():
    make_silent()
    playsound('./start.mp3')


YandexVoiceRecognition("алиса", 0, 1, action, i_listen, lambda: playsound('./stop.mp3'))
time.sleep(9999)