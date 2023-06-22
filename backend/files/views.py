from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

import requests

from .models import File
from .serializers import (
    FileUploadDisplaySerializer,
    FileUploadSerializer,
)


class FileUploadView(generics.CreateAPIView):
    permission_classes = [AllowAny] # change it later
    serializer_class = FileUploadDisplaySerializer

    def post(self, request, format=None):
        serializer = FileUploadSerializer(
            data=request.data, 
            context={'request': request})

        if serializer.is_valid():
            query_set = serializer.save()
            data = {"files": query_set}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {"detail": serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
