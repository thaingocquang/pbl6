from django.urls import path, include
from .views import trains, recognition, RecognitionAPIView

urlpatterns = [
    path('', recognition),
    path('trains', trains),
    path('test', RecognitionAPIView.as_view()),
]
