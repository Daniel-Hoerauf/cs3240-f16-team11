from django.db import models

# Create your models here.
class Report(models.Model):
    title = models.CharField(max_length = 32)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_desc = models.CharField(max_length = 100)
    long_desc = models.CharField(max_length = 256)
    files = models.FileField()
    private = models.NullBooleanField(null=True)
    username = models.CharField(max_length = 50)
    def __str__(self):
        return self.title

class Folder(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name


