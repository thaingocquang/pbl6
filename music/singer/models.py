import uuid

from django.db import models
from song.models import Song
from album.models import Album


class Singer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    songs = models.ManyToManyField(Song, related_name='singers', blank=True)
    albums = models.ManyToManyField(Album, related_name='albums', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
