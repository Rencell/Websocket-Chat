from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from channels.db import database_sync_to_async,sync_to_async
from channels.layers import get_channel_layer
from core.models import FriendRequests, Friend


@receiver(post_save, sender=FriendRequests)
def send_signal(sender, instance, created, **kwargs):
   if not created:
      if instance.status == "accepted":
         Friend.objects.create(user1=instance.user1, user2=instance.user2)
      if instance.status == "denied":
         instance.delete()
        