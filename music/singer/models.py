from django.db import models


class Singer(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
