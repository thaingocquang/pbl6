from rest_framework.utils import json
from scipy.io.wavfile import read
from song.utils.create_hashes import create_hashes
from song.utils.create_constellation import create_constellation
from song.utils.score_hashes_against_database import score_hashes_against_database
import pickle

from song.models import SongModel
from album.models import AlbumModel
from singer.models import SingerModel

from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK
import os


def song_recognize(request):
    # Save audio file to folder
    temp_audio_file = request.FILES.get('audio_file')

    if os.path.exists('songs-recognition') is False:
        os.mkdir('songs-recognition')

    # Tai file vao thu muc
    destination = open('songs-recognition/' + temp_audio_file.name, 'wb+')
    for chunk in temp_audio_file.chunks():
        destination.write(chunk)
    destination.close()

    # Bat dau nhan dien
    Fs, audio_input = read('songs-recognition/' + temp_audio_file.name)
    constellation = create_constellation(audio_input, Fs)
    hashes = create_hashes(constellation, None)

    # Load database
    database = pickle.load(open('trains-database/database.pickle', 'rb'))

    scores = score_hashes_against_database(database, hashes)[:5]

    res = []

    for song_id, score in scores:
        song = SongModel.objects.get(id=song_id)

        album = AlbumModel.objects.get(id=song.album.id)
        singers = album.singers.all()

        res_singers = []
        for s in singers:
            res_singers.append({
                "id": s.id,
                "name": s.name
            })

        res.append(
            {
                # "song_name": song.name,
                "song": {
                    "id": song.id,
                    "name": song.name,
                    "album": {
                        "id": album.id,
                        "name": album.name
                    },
                    "singers": res_singers
                },
                "score_of": score[1],
                "score_at": score[0]
            }
        )

    os.remove('songs-recognition/' + temp_audio_file.name)

    return JsonResponse({"data": res}, status=HTTP_200_OK)
    # return Response({"data": json.dumps(res, indent=4, sort_keys=True, default=str)}, HTTP_200_OK)

