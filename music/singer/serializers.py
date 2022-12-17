from rest_framework.serializers import ModelSerializer
from .models import SingerModel


class SingerSerializer(ModelSerializer):
    class Meta:
        model = SingerModel
        fields = ['id', 'name', 'age']
