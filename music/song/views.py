from rest_framework import viewsets
from .models import Song
from .serializers import SongSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from pydub import AudioSegment
from pathlib import Path
import os
from rest_framework.decorators import action


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    parser_classes = [MultiPartParser]
    serializer_class = SongSerializer

    @action(detail=True, methods=['POST'])
    def create_with_file(self, request, *args, **kwargs):
        # Get file from request
        file_obj = request.data
        temp_audio_file = request.FILES.get('audio_file')

        # Using our custom convert_to_mp3 function to obtain converted file
        converted_temp_audio_file = convert_to_mp3(temp_audio_file)

        # Adding this file to the serializer
        file_obj['audio_file'] = converted_temp_audio_file
        serializer = SongSerializer(data=file_obj)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Actual place where we save it to the MEDIA_ROOT (cloud or other)
        serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "ok"}, status.HTTP_200_OK)


def convert_to_mp3(audio_file, target_filetype='mp3', content_type='audio/mpeg', bitrate="192k"):

    file_path = audio_file.temporary_file_path()
    original_extension = file_path.split('.')[-1]
    mp3_converted_file = AudioSegment.from_file(file_path, original_extension)

    new_path = file_path[:-3] + target_filetype
    mp3_converted_file.export(new_path, format=target_filetype, bitrate="192k")

    converted_audiofile = File(
                file=open(new_path, 'rb'),
                name=Path(new_path)
            )
    converted_audiofile.name = Path(new_path).name
    converted_audiofile.content_type = content_type
    converted_audiofile.size = os.path.getsize(new_path)
    return converted_audiofile
