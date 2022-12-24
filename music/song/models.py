import os.path
import uuid

from django.db import models
from album.models import AlbumModel
import pickle
from song.utils.create_hashes import create_hashes
from song.utils.create_constellation import create_constellation
from scipy.io.wavfile import read
from music.settings import MEDIA_ROOT


def content_file_name(instance, filename):
    print("###instance", instance.audio_file)
    return os.path.join('songs', "{}".format(instance.audio_file))


class SongModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    album = models.ForeignKey(AlbumModel, on_delete=models.CASCADE)

    audio_file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    # audio_file = models.FileField(upload_to='song', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(SongModel, self).save(self, force_update, using, update_fields)

        database = {}

        if os.path.exists('trained-database') is False:
            os.mkdir('trained-database')

        if os.path.exists('trained-database/database.pickle') is True:
            with open('trained-database/database.pickle', 'rb') as f:
                database.update(pickle.load(f))


        # Read the song
        Fs, audio_input = read(MEDIA_ROOT + str(self.audio_file))

        # Create a constellation and hashes
        constellation = create_constellation(audio_input, Fs)
        hashes = create_hashes(constellation, self.id)

        # For each hash, append it to the list for this hash
        for hash, time_index_pair in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(time_index_pair)

        # ghi đè lên cái db cũ
        with open("trained-database/database.pickle", 'wb') as db:
            pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
