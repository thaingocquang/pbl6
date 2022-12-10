from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
import pickle
import numpy as np
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read
from .utils import create_constellation, create_hashes, score_hashes_against_database
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .serializers import RecognitionSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@api_view()
@action(detail=True, methods=['POST'])
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

    return Response({"message": "Thành công!"}, status.HTTP_200_OK)


@api_view()
@action(detail=True, methods=['POST'])
@parser_classes([MultiPartParser])

def recognition(request):
    # parser
    # Get file from request
    file_obj = request.data
    temp_audio_file = request.FILES.get('audio_file')

    print("file_obj", file_obj)
    print("temp_audio_file", temp_audio_file)

    return Response({"message": "ok"}, status.HTTP_200_OK)


class RecognitionAPIView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description='Upload file...',
        manual_parameters=[
            openapi.Parameter('audio_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Document to be uploaded'),
        ]
    )
    @action(detail=True, methods=['POST'])
    def post(self, request):
        r_serializer = RecognitionSerializer(data=request.data)

        if r_serializer.is_valid():
            file_obj = request.data
            temp_audio_file = request.FILES.get('audio_file')

            print("file_obj", file_obj)
            print("temp_audio_file", temp_audio_file)

            destination = open('songs-recognition/' + temp_audio_file.name, 'wb+')
            for chunk in temp_audio_file.chunks():
                destination.write(chunk)
            destination.close()  # File

            # Load the database

            database = pickle.load(open('trains-database/database.pickle', 'rb'))
            song_name_index = pickle.load(
                open("trains-database/song_index.pickle", "rb")
            )

            Fs, audio_input = read('songs-recognition/' + temp_audio_file.name)

            constellation = create_constellation.create_constellation(audio_input, Fs)
            hashes = create_hashes.create_hashes(constellation, None)

            scores = score_hashes_against_database.score_hashes_against_database(database, hashes)[:5]
            for song_id, score in scores:
                print(f"{song_name_index[song_id]}: Score of {score[1]} at {score[0]}")

            return Response({"message": "thanh cong"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "that bai"}, status=status.HTTP_400_BAD_REQUEST)


