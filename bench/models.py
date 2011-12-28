from django.db import models
from challenge.models import Challenge, UserProfile
from device.models import Device
from django.contrib.auth.models import User

PRIVACY_CHOICES = (
    ('PUBLIC', 'Publicly available'),
    ('LIMITED', 'You and challenge sponsor'),
    ('PRIVATE', 'Only you can see'),
)

class Bench(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    desc = models.CharField(max_length=2000)
    author = models.ForeignKey(User)
    #TODO: Convert from User to UserProfile
    challenge = models.ForeignKey(Challenge)
    device = models.ForeignKey(Device, default='1')
    privacy_option = models.CharField(max_length=25, choices = PRIVACY_CHOICES, default='PUBLIC')
