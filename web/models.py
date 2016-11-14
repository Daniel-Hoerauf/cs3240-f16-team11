from django.db import models


class registrationForm(models.Model):
    username = models.CharField(max_length=254, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    password = models.CharField(max_length=254, blank=False)