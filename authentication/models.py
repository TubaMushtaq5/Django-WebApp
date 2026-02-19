from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Extra fields
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True)
    def __str__(self):
        return self.username
