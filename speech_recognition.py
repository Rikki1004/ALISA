import asyncio, nest_asyncio
import threading
import websockets
import time
import uuid
import pyaudio
import json
import subprocess as sp
from datetime import datetime, timedelta
from vosk import Model, KaldiRecognizer, SetLogLevel
nest_asyncio.apply()


class YandexVoiceRecognition:
    uuuid = str(uuid.uuid4())
    translator_start_msg1 = {
        "event": {
            "header": {
                "namespace": "System",
                "name": "SynchronizeState",
                "messageId": str(uuid.uuid4()),
                "seqNumber": 1
            },
            "payload": {
                "uuid": uuuid,
                "auth_token": "bf4277fc-06c0-405a-b278-b796bbbd3f27", # это не мой токен
                "vins": {
                    "application": {
                        "lang": "ru",
                        "platform": "windows",
                        "uuid": uuuid,
                        "app_id": "ru.yandex.translate.desktop"
                    }
                }
            }
        }
    }

    translator_start_msg2 = {
        "event": {
            "header": {
                "namespace": "ASR",
                "name": "Recognize",
                "messageId": str(uuid.uuid4()),
                "streamId": 1,
                "seqNumber": 2
            },
            "payload": {
                "lang": "ru-RU",
                "streamId": 1,
                "format": "audio/webm;codecs=opus",
                "timeoutInMilliseconds": 7000,
                "punctuation": False,
                "topic": "dialogeneral"
            }
        }
    }

    alice_start_msg1 = {
        "event": {
            "header": {
                "namespace": "System",
                "name": "SynchronizeState",
                "messageId": str(uuid.uuid4()),
                "seqNumber": 1
            },
            "payload": {
                "uuid": "d0000000000004751782761711013979",
                "auth_token": "effd5a3f-fd42-4a18-83a1-61766a6d0924",
                "vins": {
                    "application": {
                        "platform": "windows",
                        "app_id": "yabro"
                    }
                }
            }
        }
    }

    alice_start_msg2 = {
        "event": {
            "header": {
                "namespace": "Vins",
                "name": "TextInput",
                "messageId": str(uuid.uuid4()),
                "seqNumber": 2
            },
            "payload": {
                "application": {
                    "app_id": "yabro",
                    "app_version": "standalone-2024-04-10-0-0",
                    "platform": "windows",
                    "os_version": "mozilla/5.0(windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/120.0.0.0 yabrowser/24.1.0.0 safari/537.36",
                    "uuid": "d0000000000004751782761711013979",
                    "lang": "ru-RU",
                    "client_time": (datetime.now() - timedelta(hours=3)).strftime("%Y%m%dT%H%M%S"),
                    "timezone": "Europe/Moscow",
                    "timestamp": str(int(time.time()))
                },
                "header": {
                    "sequence_number": None,
                    "request_id": str(uuid.uuid4()),
                    "dialog_id": None
                },
                "request": {
                    "event": {
                        "name": "@@mm_semantic_frame",
                        "payload": {
                            "typed_semantic_frame": {
                                "onboarding_get_greetings_semantic_frame": {

                                }
                            },
                            "analytics": {
                                "purpose": "get_greetings",
                                "origin": "ThisClient"
                            },
                            "request_params": {
                                "disable_output_speech": True,
                                "disable_should_listen": True,
                                "is_parallel": True
                            }
                        },
                        "type": "server_action"
                    },
                    "voice_session": False,
                    "experiments": [
                        "set_symbols_per_second=200",
                        "stroka_yabro",
                        "radio_play_in_search",
                        "search_use_cloud_ui",
                        "weather_use_cloud_ui",
                        "enable_open_link_and_cloud_ui",
                        "hw_onboarding_enable_greetings",
                        "remove_feedback_suggests",
                        "shopping_list",
                        "enable_external_skills_for_webdesktop_and_webtouch",
                        "send_show_view_directive_on_supports_show_view_layer_content_interface",
                        "use_app_host_pure_Dialogovo_scenario", "div2cards_in_external_skills_for_web_standalone"
                    ],
                    "additional_options": {
                        "bass_options": {
                            "screen_scale_factor": 1.5
                        },
                        "origin_domain": "ya.ru",
                        "supported_features": [
                            "relative_volume_change",
                            "absolute_volume_change",
                            "mute_unmute_volume",
                            "close_alice_directive",
                            "paste_text_in_field",
                            "streaming_order_android_fix",
                            "open_link",
                            "server_action",
                            "cloud_ui",
                            "cloud_first_screen_div",
                            "cloud_ui_filling",
                            "show_promo",
                            "show_view_layer_content",
                            "reminders_and_todos",
                            "div2_cards",
                            "print_text_in_message_view",
                            "player_pause_directive",
                            "supports_rich_json_cards_in_fullscreen_mode_in_skills",
                            "supports_yart_skill_image_generation"
                        ],
                        "unsupported_features": [
                            "div_cards"
                        ]
                    },
                    "location": {
                        "lat": "55.60206985473633",
                        "lon": "37.35494995117188",
                        "accuracy": "100000"
                    }
                },
                "format": "audio/ogg;codecs=opus",
                "mime": "audio/webm;codecs=opus",
                "topic": "desktopgeneral",
                "timeoutInMilliseconds": 7000
            }
        }
    }

    alice_start_msg3 = {
        "event": {
            "header": {
                "namespace": "Vins",
                "name": "VoiceInput",
                "messageId": str(uuid.uuid4()),
                "seqNumber": 3,
                "streamId": 1
            },
            "payload": {
                "application": {
                    "app_id": "yabro",
                    "app_version": "standalone-2024-04-10-0-0",
                    "platform": "windows",
                    "os_version": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/120.0.0.0 yabrowser/24.1.0.0 safari/537.36",
                    "uuid": "d0000000000004751782761711013979",
                    "lang": "ru-RU",
                    "client_time": (datetime.now() - timedelta(hours=3)).strftime("%Y%m%dT%H%M%S"),
                    "timezone": "Europe/Moscow",
                    "timestamp": str(int(time.time()))
                },
                "header": {
                    "sequence_number": None,
                    "request_id": str(uuid.uuid4()),
                    "dialog_id": None
                },
                "request": {
                    "event": {
                        "type": "voice_input"
                    },
                    "voice_session": True,
                    "experiments": [
                        "set_symbols_per_second=200",
                        "stroka_yabro",
                        "radio_play_in_search",
                        "search_use_cloud_ui",
                        "weather_use_cloud_ui",
                        "enable_open_link_and_cloud_ui",
                        "hw_onboarding_enable_greetings",
                        "remove_feedback_suggests",
                        "shopping_list",
                        "enable_external_skills_for_webdesktop_and_webtouch",
                        "send_show_view_directive_on_supports_show_view_layer_content_interface",
                        "use_app_host_pure_Dialogovo_scenario", "div2cards_in_external_skills_for_web_standalone"
                    ],
                    "additional_options": {
                        "bass_options": {
                            "screen_scale_factor": 1.5
                        },
                        "origin_domain": "ya.ru",
                        "supported_features": [
                            "relative_volume_change",
                            "absolute_volume_change",
                            "mute_unmute_volume",
                            "close_alice_directive",
                            "paste_text_in_field",
                            "streaming_order_android_fix",
                            "open_link",
                            "server_action",
                            "cloud_ui",
                            "cloud_first_screen_div",
                            "cloud_ui_filling",
                            "show_promo",
                            "show_view_layer_content",
                            "reminders_and_todos",
                            "div2_cards",
                            "print_text_in_message_view",
                            "player_pause_directive",
                            "supports_rich_json_cards_in_fullscreen_mode_in_skills",
                            "supports_yart_skill_image_generation"
                        ],
                        "unsupported_features": [
                            "div_cards"
                        ]
                    },
                    "location": {
                        "lat": "55.60206985473633",
                        "lon": "37.35494995117188",
                        "accuracy": "10000"
                    }
                },
                "format": "audio/ogg;codecs=opus",
                "mime": "audio/webm;codecs=opus",
                "topic": "desktopgeneral"
            }
        }
    }

    end_msg = {
        "streamcontrol": {
            "action": 0,
            "streamId": 3,
            "reason": 0,
            "messageId": str(uuid.uuid4())
        }
    }

    def __init__(self, activator="Алиса", service=0, offline_recognizer=0,callback_recognized=lambda: None, callback_activate=lambda: None, callback_disactivate=lambda: None):
        self.callback_activate = callback_activate
        self.callback_disactivate = callback_disactivate
        self.callback_recognized = callback_recognized
        self.activator = activator.lower()
        self.i_listen = False
        self.websocket = True
        self.service = service
        self.main_loop = asyncio.get_event_loop()

        #ffmpeg -list_devices true -f dshow -i dummy

        #self.micro = "hw:1"
        self.micro = "@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{B9E9B7ED-C923-4C07-9262-FAEF0967DC98}"
        #self.ffmpeg_driver = "alsa"
        self.ffmpeg_driver = 'dshow'

        if offline_recognizer == 0:
            threading.Thread(target=self.ffmpeg_offline_recognizer()).start()
        elif offline_recognizer == 1:
            threading.Thread(target=self.pyAudio_offline_recognizer()).start()
        else:
            raise Exception("Неверный сервис")

    def pyAudio_offline_recognizer(self):
        SetLogLevel(-1)
        model = Model("vosk-model-small-ru-0.22")
        rec = KaldiRecognizer(model, 16000)

        rec.SetWords(True)
        rec.SetMaxAlternatives(1)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        while True:
            data = stream.read(8000)
            if not rec.AcceptWaveform(data):
                result = json.loads(rec.PartialResult())
                #print(result)
                if "partial" in result and self.activator in result["partial"] and not self.i_listen:
                    f = self.ffmpeg_handler()
                    threading.Thread(target=asyncio.run, args=(f,)).start()

                    self.i_listen = True
                    rec.Reset()
                    threading.Thread(target=self.callback_activate).start() #self.callback_activate()
                    self.intermediary(self.connect_to_server)
            else:
                rec.Result()

    def ffmpeg_offline_recognizer(self):
        SetLogLevel(-1)
        model = Model("vosk-model-small-ru-0.22")
        rec = KaldiRecognizer(model, 16000)

        rec.SetWords(True)
        rec.SetMaxAlternatives(1)

        command = ["ffmpeg",
                   '-y',
                   '-f', self.ffmpeg_driver,
                   '-ac', '1',
                   '-i', "audio="+self.micro,
                   '-ac', '1',
                   '-ar', '16000',
                   '-af', "highpass=f=200, lowpass=f=3000",
                   '-b:a', '50k',
                   '-f', 'wav',
                   '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=10 ** 8)
        while True:
            data = pipe.stdout.read(8000)
            pipe.stdout.flush()
            if not rec.AcceptWaveform(data):
                result = json.loads(rec.PartialResult())
                #print(result)
                if "partial" in result and self.activator in result["partial"] and not self.i_listen:
                    f = self.ffmpeg_handler()
                    threading.Thread(target=asyncio.run, args=(f,)).start()

                    self.i_listen = True
                    rec.Reset()
                    threading.Thread(target=self.callback_activate).start() #self.callback_activate()
                    self.intermediary(self.connect_to_server)
                    pipe.stdout.flush()
            else:
                rec.Result()

    async def ffmpeg_handler(self):
        command = ["ffmpeg",
                   '-y',
                   '-f', self.ffmpeg_driver,
                   '-ac', '1',
                   '-i', "audio="+self.micro,
                   '-ac', '1',
                   '-af', "highpass=f=200, lowpass=f=3000",
                   '-ar', '16000',
                   '-c:a', 'libopus',
                   '-b:a', '50k',
                   '-f', 'webm',
                   '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=10 ** 8)
        while True:
            if not self.websocket:
                time.sleep(0.1)
                continue
            raw_audio = pipe.stdout.read(2048)
            pipe.stdout.flush()

            try:
                await self.websocket.send(b"\x00\x00\x00\x01" + raw_audio)
            except Exception as e:
                pipe.terminate()
                break

    def intermediary(self, f, arg1=None, arg2=None):
        asyncio.set_event_loop(self.main_loop)
        if arg1 and arg2:
            asyncio.run(f(arg1, arg2))
        elif arg1 and not arg2:
            asyncio.run(f(arg1))
        elif arg2 and not arg1:
            asyncio.run(f(arg2))
        else:
            asyncio.run(f())

    async def receiver(self, websocket):
        while 1 == 1:
            try:
                recv = await websocket.recv()
                ans = json.loads(recv)
                if ("directive" in ans and "recognition" in ans["directive"]["payload"] and len(
                        ans["directive"]["payload"][
                            "recognition"]) > 0):  # and ans["directive"]["payload"]["recognition"][0]["confidence"] < 100):
                    words = ans["directive"]["payload"]["recognition"][0]["normalized"]
                    raw_words = [x["value"].strip().lower() for x in
                                 ans["directive"]["payload"]["recognition"][0]["words"]]
                    #print(raw_words)
                    if (ans["directive"]["payload"]["endOfUtt"]):
                        self.i_listen = False
                        if(not words.lower().strip()):
                            break
                        threading.Thread(target=self.callback_recognized,args=(words.lower().strip(),)).start() #self.callback_recognized(words.lower().strip())
                        break
            except Exception as e:
                print("receiver: ", e)
                time.sleep(0.1)
                break

    async def connect_to_server(self):
        try:
            #wss://uniproxy.alice.yandex.net/uni.ws
            #wss://uniproxy.alice.ya.ru/uni.ws
            async with websockets.connect("wss://uniproxy.alice.ya.ru/uni.ws") as websocket:
                self.websocket = websocket
                if self.service == 0:
                    await websocket.send(json.dumps(self.alice_start_msg1))
                    await websocket.send(json.dumps(self.alice_start_msg2))
                    await websocket.send(json.dumps(self.alice_start_msg3))
                    await websocket.recv()
                elif self.service == 1:
                    await websocket.send(json.dumps(self.translator_start_msg1))
                    await websocket.send(json.dumps(self.translator_start_msg2))
                else:
                    raise Exception("Неверный сервис")

                #f = self.ffmpeg_handler(websocket)
                #threading.Thread(target=asyncio.run, args=(f,)).start()

                await self.receiver(websocket)
                await websocket.send(json.dumps(self.end_msg))
            self.websocket = True
        except Exception as e:
            print("connect_to_server: ", e)
        self.callback_disactivate()



"""
def printo(text):
    print("final: ", text)
def printo2():
    print("я слушаю")
def printo3():
    print("я перестала слушать")

YandexVoiceRecognition("алиса", 0, 0, printo, printo2, printo3)
time.sleep(9999)
"""
