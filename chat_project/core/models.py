from django.db import models
from Accounts.models import User


class Room(models.Model):
    name = models.TextField
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name
