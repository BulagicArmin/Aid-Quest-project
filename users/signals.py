from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User, Donator

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.staff==True:
        Profile.objects.create(user=instance)
    elif created and instance.staff==False:
        Donator.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.staff==True:
        instance.profile.save()
    else:
        instance.donator.save()


