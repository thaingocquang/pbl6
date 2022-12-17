from django.shortcuts import render
from rest_framework import viewsets
from .models import SingerModel
from .serializers import SingerSerializer


class SingerViewSet(viewsets.ModelViewSet):
    queryset = SingerModel.objects.all()
    serializer_class = SingerSerializer

