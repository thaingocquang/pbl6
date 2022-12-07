from rest_framework.serializers import ModelSerializer
from .models import Song

from rest_framework import serializers
from django.core.validators import FileExtensionValidator


class SongSerializer(ModelSerializer):
    # singers = SingerSerializer(many=True, read_only=True)
    audio_file = serializers.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['flac', 'mov', 'wav', 'mp3'])
        ]
    )

    class Meta:
        model = Song
        # fields = ['id', 'name', 'album']
        fields = '__all__'


# class PodcastSerializer(serializers.ModelSerializer):
#     # This does not validate the content of the data itself, just the extension!
#     audio_file = serializers.FileField(
#         validators=[
#             FileExtensionValidator(allowed_extensions=['flac', 'mov', 'wav', 'mp3'])
#         ]
#     )
#
#     class Meta:
#         model = Podcast
#         # read_only_fields = 'id'
#         fields = '__all__'
