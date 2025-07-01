from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    language = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    reporting = models.ForeignKey('self',on_delete=models.CASCADE,null=True, related_name='reporting_empid')

class Message(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.content[:20]}"