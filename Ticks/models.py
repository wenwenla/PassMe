from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    partner = models.OneToOneField('Profile', null=True, on_delete=models.CASCADE)
    introduce = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=BaseUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Event(models.Model):
    CLASS = (
        ('W', 'WAKE_UP'),
        ('S', 'SLEEP'),
        ('O', 'OTHER'),
    )

    title = models.CharField(max_length=10)
    content = models.CharField(max_length=128)
    class_type = models.CharField(max_length=1, choices=CLASS, default='O')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
