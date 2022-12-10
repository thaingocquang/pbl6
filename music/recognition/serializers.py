from rest_framework import serializers
from django.core.validators import FileExtensionValidator


class RecognitionSerializer(serializers.Serializer):
    audio_file = serializers.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['flac', 'mov', 'wav', 'mp3'])
        ]
    )
