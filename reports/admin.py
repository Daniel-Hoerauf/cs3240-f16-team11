from django.contrib import admin
from .models import Report, UploadedFile, Folder

admin.site.register(Report)
admin.site.register(UploadedFile)
admin.site.register(Folder)
