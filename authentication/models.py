from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def clean(self):
    #     # Only email uniqueness
    #     if CustomUser.objects.exclude(pk=self.pk).filter(email=self.email).exists():
    #         print("MODEL-LEVEL: Email already exists!")   
    #         raise ValidationError({'email': "A user with this email already existss."})

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username
