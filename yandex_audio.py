from yandex_music import Client
import time

moya_musica_offset = 0
client = Client("токен яндекс музыки").init()
volnaParams = {
    "name": "user:onyourwave",
    "batch_id": None,
    "1stTrack": None,
    "2stTrack": None,
    "total_played_seconds": None
}


def moya_volna(trackHistory=[]):
    if (volnaParams["batch_id"]):
        client.rotor_station_feedback_track_finished(volnaParams["name"], volnaParams["1stTrack"],
                                                     volnaParams["total_played_seconds"], volnaParams["batch_id"],
                                                     time.time())
        client.rotor_station_feedback_track_started(volnaParams["name"], volnaParams["2stTrack"],
                                                    volnaParams["batch_id"], time.time())

    rotor = client.rotorStationTracks(volnaParams["name"], queue=volnaParams["1stTrack"]).to_dict()

    reserve_tracks = [rotor["sequence"][-2]["track"]["id"], rotor["sequence"][-1]["track"]["id"]]
    for i in rotor["sequence"]:
        for ii in trackHistory:
            if i["track"]["title"] in ii["title"]:
                rotor["sequence"].remove(i)

    if (len(rotor["sequence"]) <= 2):
        volnaParams["1stTrack"] = reserve_tracks[0]
        volnaParams["2stTrack"] = reserve_tracks[1]
    else:
        volnaParams["1stTrack"] = rotor["sequence"][0]["track"]["id"]
        volnaParams["2stTrack"] = rotor["sequence"][1]["track"]["id"]
    volnaParams["batch_id"] = rotor["batch_id"]

    track = client.tracks(volnaParams["1stTrack"])[0]
    url = track.getDownloadInfo(True)[0]["direct_link"]

    duration = track.duration_ms

    volnaParams["total_played_seconds"] = int(duration / 1000) if duration else 100

    result = {
        "title": rotor["sequence"][0]["track"]["title"],
        "artist": rotor["sequence"][0]["track"]["artists"][0]["name"],
        "url": url
    }
    return result


def moya_musica(curTrackList, f=None):
    global moya_musica_offset
    curTrackList.clear()

    audios = client.users_likes_tracks().fetch_tracks()

    for i in audios[moya_musica_offset:moya_musica_offset + 10]:
        curTrackList.append({
            "title": i.title,
            "artist": i.artists[0].name,
            "url": i.getDownloadInfo(True)[0]["direct_link"]
        })

    moya_musica_offset += 10

    if (f and len(curTrackList) > 0):
        f()


def find(curTrackList, query, f=None):
    results = client.search(query, False, "track", 0, False).tracks.results

    for i in results:
        curTrackList.append({
            "title": i.title,
            "artist": i.artists[0].name,
            "url": i.getDownloadInfo(True)[0]["direct_link"]
        })

    if f:
        f()
