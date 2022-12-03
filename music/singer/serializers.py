from rest_framework.serializers import ModelSerializer
from .models import Singer


class SingerSerializer(ModelSerializer):
    class Meta:
        model = Singer
        fields = ['name', 'age']