from django.db import models as m

# Create your models here.
class Report(m.Model):
    title = m.CharField(max_length = 256) #If there is a limit, say m.CharField(max_length = 256 or whatever the max length is)
    timestamp = m.TimeField()
    short_desc = m.CharField(max_length = 256)
    long_desc = m.CharField(max_length = 256)
    files = m.CharField(max_length = 256)
    private = m.BooleanField(max_length = 256)
    username = m.CharField(max_length = 256)
