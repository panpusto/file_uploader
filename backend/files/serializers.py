from rest_framework import serializers

from .models import File


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'file'
        ]


class FileUploadField(serializers.FileField):
    def to_internal_value(self, data):
        if not data:
            return None
        
        max_size = 10 * 1024 * 1024 # 10MB

        if data.size > max_size:
            raise serializers.ValidationError('File size exceeds the limit.')
        
        return data
    
    def to_representation(self, value):
        if not value:
            return None
        return value.url


class MultipleFileCreateSerializer(serializers.Serializer):
    files = serializers.ListField(child=FileUploadField(write_only=True), write_only=True)
    download_links = serializers.ListField(child=serializers.URLField(), read_only=True)
