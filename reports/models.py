from django.db import models
from django.contrib.auth.models import User
from web.models import UserGroup


def get_file_dest(instance, filename):
    return '{}/{}/{}'.format(instance.owner.pk,
                             instance.owner.last_login,
                             filename)


# Create your models here.
class Report(models.Model):
    title = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    # files = models.FileField(null=True, blank=True,
    # upload_to=get_file_dest)
    files_encrypted = models.BooleanField(default=False)
    keyword = models.CharField(max_length=32, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                              )

    def __str__(self):
        return self.title


class UploadedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name='file_set')
    file_obj = models.FileField(upload_to=get_file_dest)

    def __str__(self):
        return self.file_obj.name

class Folder(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
