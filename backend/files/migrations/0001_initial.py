# Generated by Django 4.2.1 on 2023-06-20 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import files.utils
import files.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=255, upload_to=files.utils.path_to_upload_file)),
                ('link', models.CharField(max_length=255)),
                ('time_to_expired', models.IntegerField(validators=[files.validators.validate_time_to_expired])),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]