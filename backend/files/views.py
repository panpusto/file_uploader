from rest_framework import generics, status
from rest_framework.response import Response
from .models import File
from .serializers import MultipleFileCreateSerializer


class FileCreateAPIView(generics.CreateAPIView):
    serializer_class = MultipleFileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            files = serializer.validated_data['files']
            download_links = []
            base_url = request.build_absolute_uri('/')


            for file in files:
                file_instance = File(user=request.user, file=file)
                file_instance.save()

                download_links.append(base_url + file_instance.file.url.lstrip('/'))
            
            return Response({'download_links': download_links}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
