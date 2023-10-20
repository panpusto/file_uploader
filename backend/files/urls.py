from django.urls import path
from .views import FileCreateAPIView


urlpatterns = [
    path('', FileCreateAPIView.as_view(), name='files'),
]
