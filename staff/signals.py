from django.db.models.signals import post_save

from django.contrib.auth.models import NewUser

from django.dispatch import receiver
from .models import Restaurant


@receiver(post_save,sender=NewUser)
def create_profile(sender, instance,created,**kwarfs):
	if created:
		Restaurant.objects.create(user=instance)
