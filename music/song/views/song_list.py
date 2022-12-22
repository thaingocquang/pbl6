from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from song.models import SongModel
from song.serializers import SongSerializer


def song_list():
    songs = SongModel.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response({"data": serializer.data}, status=HTTP_200_OK)