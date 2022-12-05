from rest_framework.serializers import ModelSerializer
from .models import Song
from singer.serializers import SingerSerializer


class SongSerializer(ModelSerializer):
    # singers = SingerSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'name', 'album']
