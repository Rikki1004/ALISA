import asyncio, nest_asyncio
import subprocess
import websockets
import os
import uuid
import subprocess as sp
import json

nest_asyncio.apply()


class YandexVoiceGenerator:
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
                "namespace": "TTS",
                "name": "Generate",
                "messageId": str(uuid.uuid4()),
                "seqNumber": 2
            },
            "payload": {
                "text": "|text|",
                "lang": "ru",
                "voice": "|voice|",
                "format": "audio/ogg;codecs=opus"
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

    def __init__(self, voice="oksana.gpu"):
        self.voiceName = voice

    async def vocalize(self, file_bytes):
        temp_audio_file = 'temp_audio.ogg'
        with open(temp_audio_file, 'wb') as f:
            f.write(file_bytes)
        command = ["ffplay", '-nodisp', '-autoexit', "./" + temp_audio_file]
        subprocess.run(command, stderr=sp.DEVNULL)
        os.remove(temp_audio_file)

    def voice(self, text):
        asyncio.run(self._voice(text))

    async def _voice(self, text):
        try:
            # wss://uniproxy.alice.yandex.net/uni.ws
            # wss://uniproxy.alice.ya.ru/uni.ws
            async with websockets.connect("wss://uniproxy.alice.yandex.net/uni.ws") as websocket:
                await websocket.send(json.dumps(self.translator_start_msg1))
                await websocket.send(
                    json.dumps(self.translator_start_msg2).replace("|text|", text).replace("|voice|", self.voiceName))

                bytes_of_sound = b""
                while 1 == 1:
                    msg = await websocket.recv()
                    if type(msg) == bytes:
                        bytes_of_sound += msg
                    else:
                        if "directive" in json.loads(msg):
                            pass
                        elif "streamcontrol" in json.loads(msg):
                            await self.vocalize(bytes_of_sound)
                            break

        except Exception as e:
            print("connect_to_server: ", e)

# a = YandexVoiceGenerator()
# a.voice("переключаюсь на vk")
# time.sleep(9999)
