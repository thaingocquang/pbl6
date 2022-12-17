from rest_framework import viewsets
from .models import AlbumModel
from .serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = AlbumModel.objects.all()
    serializer_class = AlbumSerializer

