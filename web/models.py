from django.db import models
from django.contrib.auth.models import User as Users

# Create your models here.

class UserGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True, default='GROUP')
    members = models.ManyToManyField(Users)

    def __str__(self):
        return self.name
