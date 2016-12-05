from django.contrib import admin
from .models import Report, UploadedFile

# Register your models here.
admin.site.register(Report)
admin.site.register(UploadedFile)
