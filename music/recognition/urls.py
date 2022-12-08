from django.urls import path, include
from .views import trains

urlpatterns = [
    path('trains', trains),
]
