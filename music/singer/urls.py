from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SingerViewSet

router = DefaultRouter()
router.register('singers', SingerViewSet)

urlpatterns = [
    path('', include(router.urls))
]