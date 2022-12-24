import uuid

from django.db import models
from singer.models import SingerModel


class AlbumModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    # singer = models.ManyToManyField(SingerModel, blank=True)
    singer = models.ForeignKey(SingerModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
