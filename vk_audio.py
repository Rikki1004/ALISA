import requests
import re
import base64
import hashlib
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

token = "" # токен вк музыки для моей волны
moya_musica_offset = 0
endpoint = "https://kissvk.me/api/getContent"
myId = 1234567 # id вк

def moya_volna(trackHistory=None):
    url = "https://api.vk.com/method/audio.getStreamMixAudios?v=5.226&client_id=6287487"
    data = {
        "mix_id": "common",
        "count": 1,
        "access_token": token
    }
    r = requests.post(url, data=data).json()
    result = {
        "title": r["response"][0]["title"],
        "artist": r["response"][0]["artist"],
        "url": r["response"][0]["url"]
    }
    return result


def moya_musica(curTrackList, f=None):
    global moya_musica_offset
    curTrackList.clear()
    data = {
        "count": 30,
        "offset": moya_musica_offset,
        "url": f"/audios{myId}",
        "action": "scroll"
    }
    moya_musica_offset += 30
    r = requests.post(endpoint, data=data).json()
    soup = BeautifulSoup(r["html"], 'html.parser')
    audios = soup.find_all("div", "audio")
    for i in audios:
        try:
            curTrackList.append({
                "title": i.find("div", "title").text,
                "artist": i.find("div", "author").a.text,
                "url": decoder(i["data-audio"])
            })
        except Exception as e:
            pass

    if f and len(curTrackList) > 0:
        f()


def decoder(code):
    code_parts = code.split(":")
    ct = base64.b64decode(code_parts[0])
    iv = bytes.fromhex(code_parts[1])
    salt = bytes.fromhex(code_parts[2])

    pass_phrase = b"kissvk.me"

    md = hashlib.md5()
    md.update(pass_phrase)
    md.update(salt)
    cache0 = md.digest()

    md = hashlib.md5()
    md.update(cache0)
    md.update(pass_phrase)
    md.update(salt)
    cache1 = md.digest()

    key = cache0 + cache1

    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = re.sub(r'[^\x20-\x7E]', '', cipher.decrypt(ct).decode('utf-8').strip().replace("\\/", "/"))[1:-1]
    return result


def find(curTrackList, query, f=None):
    data = {
        "count": 30,
        "offset": 0,
        "url": f"/audios{myId}?q={query}",
        "action": "search"
    }
    r = requests.post(endpoint, data=data).json()
    soup = BeautifulSoup(r["html"], 'html.parser')
    audios = soup.find_all("div", "audio")

    for i in audios:
        try:
            curTrackList.append({
                "title": i.find("div", "title").text,
                "artist": i.find("div", "author").a.text,
                "url": decoder(i["data-audio"])
            })
        except Exception as e:
            pass

    if f:
        f()
