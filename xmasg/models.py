from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    '''
    Class for Room = Stanza
    '''
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()       # final date (for countdown)
    admin = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.name}"