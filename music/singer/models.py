import uuid

from django.db import models
from django.utils.html import mark_safe


class SingerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    # songs = models.ManyToManyField(Song, related_name='singers', blank=True)
    # albums = models.ManyToManyField(Album, related_name='albums', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def avatar_preview(self):
        print("@@@", mark_safe('<img src="media/{url}" width="300" height="300" />'.format(url=self.avatar)))
        if self.avatar:
            return mark_safe('<img src="/media/{url}" width="300" height="300" />'.format(url=self.avatar))
        return ""
