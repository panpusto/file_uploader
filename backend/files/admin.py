from django.contrib import admin

from .models import File, Archive


admin.site.register(Archive)
admin.site.register(File)