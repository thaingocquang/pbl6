from rest_framework.serializers import ModelSerializer
from .models import Album
from singer.serializers import SingerSerializer


class AlbumSerializer(ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'name', 'singers']
