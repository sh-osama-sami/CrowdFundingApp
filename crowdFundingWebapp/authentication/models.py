from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class CustomUser(User):
    mobile_phone = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
