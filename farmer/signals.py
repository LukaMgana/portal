from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Farmer
from django.contrib import messages

@receiver(post_save, sender = User)
def post_save_created_farmer(sender, instance, created, **kwargs):
    if created:
        Farmer.objects.create(
            user=instance, 
            full_name = str(instance.first_name + " "+instance.last_name), 
            email =instance.email,
            )
            