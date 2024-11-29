from django.db import models
from Accounts.models import User
from django.utils.text import slugify


class Room(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Message(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message