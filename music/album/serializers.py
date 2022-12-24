from rest_framework.serializers import ModelSerializer
from .models import AlbumModel
from singer.serializers import SingerSerializer


class AlbumSerializer(ModelSerializer):

    class Meta:
        model = AlbumModel
        fields = ['id', 'name', 'singer']
