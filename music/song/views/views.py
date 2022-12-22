from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from .song_create import song_create
from .song_recognize import song_recognize
from .song_list import song_list
from .song_update import song_update


class SongAPIView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description='Thêm bài hát...',
        manual_parameters=[
            openapi.Parameter('audio_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Tải bài hát lên...'),
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song name'),
            openapi.Parameter('album', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song album'),
        ]
    )
    @action(detail=True, methods=['POST'])
    def post(self, request):
        return song_create(request)

    def get(self, request):
        return song_list()

    # @swagger_auto_schema(
    #     operation_description='Chỉnh sửa bài hát...',
    #     manual_parameters=[
    #         openapi.Parameter('audio_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Tải bài hát lên...'),
    #         openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song name'),
    #         openapi.Parameter('album', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Song album'),
    #     ]
    # )
    # @action(detail=True, methods=['POST'])
    # def put(self, request):
    #     return song_update()

@swagger_auto_schema(
    method='POST',
    operation_description='Nhận diện bài hát...',
    manual_parameters=[
        openapi.Parameter('audio_file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Tải đoạn nhạc hoặc bài hát để nhận diện ...'),
    ],
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def recognize(request):
    return song_recognize(request)

