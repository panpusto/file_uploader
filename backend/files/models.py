import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .utils import path_to_upload_file
from .validators import validate_time_to_expired



class File(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.FileField(upload_to=path_to_upload_file, max_length=255)
    link = models.CharField(max_length=255)
    time_to_expired = models.IntegerField(validators=[validate_time_to_expired])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
