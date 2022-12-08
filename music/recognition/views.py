from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view
import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
import pickle
import numpy as np
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read
from .utils import create_constellation, create_hashes


@api_view()
def trains(request):
    songs = glob.glob('songs-stored/*.wav')

    song_name_index = {}
    database: Dict[int, List[Tuple[int, int]]] = {}

    # Go through each song, using where they are alphabetically as an id
    for index, filename in enumerate(tqdm(sorted(songs))):
        song_name_index[index] = filename

        # Read the song, create a constellation and hashes
        Fs, audio_input = read(filename)
        constellation = create_constellation.create_constellation(audio_input, Fs)
        hashes = create_hashes.create_hashes(constellation, index)

        # For each hash, append it to the list for this hash
        for hash, time_index_pair in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(time_index_pair)

    # Dump the database and list of songs as pickles
    with open("trains-database/database.pickle", 'wb') as db:
        pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
    with open("trains-database/song_index.pickle", 'wb') as songs:
        pickle.dump(song_name_index, songs, pickle.HIGHEST_PROTOCOL)

    return Response({"message": "Hello Quang!"}, HTTP_200_OK)


class RecognitionAPIView(APIView):
    def get(self, request):

        return Response({"message": "Thành công!"}, HTTP_200_OK)
        # path = "/content/drive/MyDrive/Colab Notebooks/"
        # songs = glob.glob(path + 'data_wav_filtered_downsampling/*.wav')
        #
        # song_name_index = {}
        # database: Dict[int, List[Tuple[int, int]]] = {}
        #
        # # Go through each song, using where they are alphabetically as an id
        # for index, filename in enumerate(tqdm(sorted(songs))):
        #     song_name_index[index] = filename
        #     # Read the song, create a constellation and hashes
        #     Fs, audio_input = read(filename)
        #     constellation = create_constellation(audio_input, Fs)
        #     hashes = create_hashes(constellation, index)
        #
        #     # For each hash, append it to the list for this hash
        #     for hash, time_index_pair in hashes.items():
        #         if hash not in database:
        #             database[hash] = []
        #         database[hash].append(time_index_pair)
        # # Dump the database and list of songs as pickles
        # with open("/content/drive/MyDrive/Colab Notebooks/Database/database.pickle", 'wb') as db:
        #     pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
        # with open("/content/drive/MyDrive/Colab Notebooks/Database/song_index.pickle", 'wb') as songs:
        #     pickle.dump(song_name_index, songs, pickle.HIGHEST_PROTOCOL)
        # # return Response(usernames)
