from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# 1. The Creation Signal


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # get_or_create safely checks the database first.
        # This completely prevents the UNIQUE constraint IntegrityError!
        Profile.objects.get_or_create(user=instance)

# 2. The Save Signal


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # We use a try/except block as a safety net.
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # If the profile somehow didn't exist when the user was saved,
        # we catch the error and safely create it here.
        Profile.objects.get_or_create(user=instance)
