import uuid

from django.db import models
from django.contrib.auth import get_user_model

from pathlib import Path 

from .utils import path_to_upload_file
from .validators import validate_time_to_expired


class Archive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    files = models.ManyToManyField('File')
    zip_file_link = models.CharField(max_length=255)
    expiration_time = models.IntegerField(validators=[validate_time_to_expired])
    creation_date = models.DateField(auto_now_add=True)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=path_to_upload_file, max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)

    def get_filename(self):
        return Path(f'{self.file}').stem
    
    def __str__(self):
        return f'{self.get_filename()}'
    