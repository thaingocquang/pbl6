import os.path
import uuid

from django.db import models
from album.models import AlbumModel


def content_file_name(instance, filename):
    print("###instance", instance.audio_file)
    return os.path.join('songs-stored', "{}".format(instance.audio_file))


class SongModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    album = models.ForeignKey(AlbumModel, on_delete=models.CASCADE)

    audio_file = models.FileField(upload_to=content_file_name, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
