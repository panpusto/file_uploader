from rest_framework import serializers

from .models import File


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
        allow_empty_file=False,
        use_url=False
    ))

    class Meta:
        model = File
        fields = [
            'file'
        ]
    
    def create(self, validated_data):
        file=validated_data.pop('file')
        user=self.context['request'].user

        file_list = []
        for item in file:
            f = File.objects.create(file=item, user=user)
            f_url = f'{f.file.url}'
            file_list.append(f_url)
            
        return file_list


class FileUploadDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
