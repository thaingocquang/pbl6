from django.shortcuts import render
from rest_framework import viewsets
from .models import Singer
from .serializers import SingerSerializer


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.filter()
    serializer_class = SingerSerializer

