import os.path

from rest_framework.response import Response
from song.serializers import SongSerializer
from scipy.io.wavfile import read, write
import librosa
import numpy as np
from scipy.signal import butter,filtfilt
from song.utils.create_hashes import create_hashes
from song.utils.create_constellation import create_constellation
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import pickle

from song.utils.file_handle import save_audio_file_into_folder


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
    write("songs-temp/" + "song-temp.wav", 11025,
          scaled)  # Lưu tạm ở đâu đấy với tên cố định luôn như test hay raw gì đấy


def song_create(request):
    serializer = SongSerializer(data=request.data)

    # If serialize fail
    if not serializer.is_valid():
        return Response(
            {"errors": serializer.errors},
            HTTP_400_BAD_REQUEST
        )
    instance = serializer.save()

    # Save audio file to folder
    temp_audio_file = request.FILES.get('audio_file')
    save_audio_file_into_folder(
        temp_audio_file=temp_audio_file,
        path_to_folder='songs-stored',
        file_name=temp_audio_file.name
    )

    # handle('songs-stored/' + temp_audio_file.name)

    database = {}

    if os.path.exists('trains-database') is False:
        os.mkdir('trains-database')

    if os.path.exists('trains-database/database.pickle') is True:
        with open('trains-database/database.pickle', 'rb') as f:
            database.update(pickle.load(f))

    # filename = "songs-temp/" + "song-temp.wav"  # Cái file lưu tạm lúc nãy

    # Read the song
    Fs, audio_input = read('songs-stored/' + temp_audio_file.name)

    # Create a constellation and hashes
    constellation = create_constellation(audio_input, Fs)
    hashes = create_hashes(constellation, instance.id)

    print(hashes)

    # For each hash, append it to the list for this hash
    for hash, time_index_pair in hashes.items():
        if hash not in database:
            database[hash] = []
        database[hash].append(time_index_pair)

    # ghi đè lên cái db cũ
    with open("trains-database/database.pickle", 'wb') as db:
        pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)

    # xoa file trong file temp
    # os.remove('songs-temp/song-temp.wav')

    return Response(
        {"data": serializer.data},
        HTTP_200_OK
    )
