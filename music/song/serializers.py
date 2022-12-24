from rest_framework.serializers import ModelSerializer
from .models import SongModel

from rest_framework import serializers
from django.core.validators import FileExtensionValidator


class SongSerializer(ModelSerializer):
    # singers = SingerSerializer(many=True, read_only=True)
    audio_file = serializers.FileField(
        validators=[
            # FileExtensionValidator(allowed_extensions=['flac', 'mov', 'wav', 'mp3']),
            FileExtensionValidator(allowed_extensions=['wav']),
        ]
    )

    class Meta:
        model = SongModel
        # fields = ['id', 'name', 'album']
        fields = '__all__'

    def create(self, validated_data):
        print("HELLO")


class SongRecogSerializer(serializers.Serializer):
    audio_file = serializers.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['flac', 'mov', 'wav', 'mp3'])
        ]
    )


class SongRecognizeResponseSerializer(serializers.Serializer):
    song = SongModel
    score_of = serializers.IntegerField
    score_at = serializers.IntegerField
