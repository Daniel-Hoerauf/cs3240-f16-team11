from django.db import models

# Create your models here.
class Report(models.Model):
    title = models.CharField(max_length = 32)
    timestamp = models.DateTimeField('date created')
    short_desc = models.CharField(max_length = 100)
    long_desc = models.CharField(max_length = 256)
    files = models.CharField(max_length = 500)
    private = models.BooleanField()
    username = models.CharField(max_length = 50)
    def __str__(self):
        return self.title


