import scipy.signal
from rest_framework import viewsets
from .models import SongModel
from .serializers import SongSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from pydub import AudioSegment
from pathlib import Path
import os
from rest_framework.decorators import action
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from scipy.signal import butter, filtfilt
import librosa
import numpy as np
from scipy.io.wavfile import read, write
from recognition.utils.create_constellation import create_constellation
from recognition.utils.create_hashes import create_hashes

class SongViewSet(viewsets.ModelViewSet):
    queryset = SongModel.objects.all()
    parser_classes = [MultiPartParser]
    serializer_class = SongSerializer

    def create(self, request, *args, **kwargs):
        return Response({"message": "Hello Quang"}, status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def create_with_file(self, request, *args, **kwargs):
        # Get file from request
        file_obj = request.data
        temp_audio_file = request.FILES.get('audio_file')

        # Using our custom convert_to_mp3 function to obtain converted file
        converted_temp_audio_file = convert_to_mp3(temp_audio_file)

        # Adding this file to the serializer
        file_obj['audio_file'] = converted_temp_audio_file
        serializer = SongSerializer(data=file_obj)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Actual place where we save it to the MEDIA_ROOT (cloud or other)
        serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "ok"}, status.HTTP_200_OK)


def convert_to_mp3(audio_file, target_filetype='mp3', content_type='audio/mpeg', bitrate="192k"):
    file_path = audio_file.temporary_file_path()
    original_extension = file_path.split('.')[-1]
    mp3_converted_file = AudioSegment.from_file(file_path, original_extension)

    new_path = file_path[:-3] + target_filetype
    mp3_converted_file.export(new_path, format=target_filetype, bitrate="192k")

    converted_audiofile = File(
        file=open(new_path, 'rb'),
        name=Path(new_path)
    )
    converted_audiofile.name = Path(new_path).name
    converted_audiofile.content_type = content_type
    converted_audiofile.size = os.path.getsize(new_path)
    return converted_audiofile


from .serializers import SongSerializer


# def butter_lowpass_filter(data, cutoff, fs, order):
#     normal_cutoff = cutoff / nyq
#     # Get the filter coefficients
#     # scipy.signal.butter()
#
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     y = filtfilt(b, a, data)
#     return y

def handle(song_name):
    songfile, sr = librosa.load(song_name)  # Chỗ đưa bài từ API vào
    cutoff = 5000  # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
    nyq = 0.5 * sr  # Nyquist Frequency
    order = 2  # sin wave can be approx represented as quadratic
    number_of_samples = round(len(songfile) * float(10700) / sr)
    # y = butter_lowpass_filter(songfile, cutoff, sr, order)

    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    # scipy.signal.butter()

    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, songfile)

    data = librosa.resample(y, orig_sr=sr, target_sr=11025)
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    write("songs-temp/" + "song-temp.wav", 11025, scaled)  # Lưu tạm ở đâu đấy với tên cố định luôn như test hay raw gì đấy

class SongAPIView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description='Upload file...',
        manual_parameters=[
            openapi.Parameter('audio_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Document to be uploaded'),
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song name'),
            openapi.Parameter('album', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song album'),
        ]
    )
    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = SongSerializer(data=request.data)

        # If serialize fail
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status.HTTP_400_BAD_REQUEST
            )
        instance = serializer.save()

        # Save audio file to folder
        temp_audio_file = request.FILES.get('audio_file')
        destination = open('songs-stored/' + temp_audio_file.name, 'wb+')
        for chunk in temp_audio_file.chunks():
            destination.write(chunk)
        destination.close()

        handle('songs-stored/' + temp_audio_file.name)

        # Load the database
        import pickle
        database = {}
        song_name_index = {}
        with open('trains-database/database.pickle', 'rb') as f:
            database.update(pickle.load(f))

        filename = "songs-temp/" + "song-temp.wav" # Cái file lưu tạm lúc nãy

        # Read the song
        Fs, audio_input = read(filename)

        # Create a constellation and hashes
        constellation = create_constellation(audio_input, Fs)
        hashes = create_hashes(constellation, instance.id)

        # For each hash, append it to the list for this hash
        for hash, time_index_pair in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(time_index_pair)

        # ghi đè lên cái db cũ
        with open("trains-database/database.pickle", 'wb') as db:
            pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)

        return Response(
            {"data": serializer.data},
            status.HTTP_200_OK
        )
