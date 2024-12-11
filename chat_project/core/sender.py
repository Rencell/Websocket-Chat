from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer


@receiver(post_save, sender=None)
async def send_signal(sender, instance, created, **kwargs):
   pass
        