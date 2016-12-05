from django.db import models
from django.contrib.auth.models import User
from web.models import UserGroup


def get_file_dest(instance, filename):
    return 'user_{}/{}/{}/{}'.format(instance.owner.pk, instance.timestamp.minute,
                                     instance.timestamp.second, filename)


# Create your models here.
class Report(models.Model):
    title = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    files = models.FileField(null=True, blank=True,
                             upload_to=get_file_dest)
    file_encrypted = models.BooleanField(default=False)
    keyword = models.CharField(max_length=32, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                              )

    def __str__(self):
        return self.title


class Folder(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
