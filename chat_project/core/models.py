from django.db import models
from Accounts.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Friend(models.Model):
    user1 = models.ForeignKey(User, related_name='friend_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError("You can not add yourself, do you even have friends?")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friendship')
        ]
       
class conversation(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
