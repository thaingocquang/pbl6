from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .viewss import SongViewSet, SongAPIView
from .views.views import SongAPIView, recognize

# router = DefaultRouter()
# router.register('songs', SongViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('song-api-view', SongAPIView.as_view()),
    path('recognize', recognize)
]
