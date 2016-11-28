from django.db import models
from django.contrib.auth.models import User as Users

# Create your models here.

class UserGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True, default='GROUP')
    members = models.ManyToManyField(Users)

    def __str__(self):
        return self.name

class Message(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    recipient = models.ForeignKey(Users, on_delete=models.CASCADE,
                                  related_name='message_to')
    sender = models.ForeignKey(Users, on_delete=models.CASCADE,
                               related_name='message_from')
    read = models.BooleanField()
    encrypted = models.BooleanField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}--{} ({})'.format(self.subject, self.sender, self.sent)
