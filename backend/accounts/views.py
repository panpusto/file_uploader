from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterAccountSerializer

class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterAccountSerializer
