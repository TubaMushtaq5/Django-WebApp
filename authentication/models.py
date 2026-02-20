from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
import django.utils.timezone as timezone
import pytz

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class PSTDateTimeRecord(models.Model):
    title = models.CharField(max_length=255)
    datetime_pst = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Ensure datetime_pst is stored in PST consistently:
        - If naive, assume UTC
        - Convert to PST before saving
        """
        if self.datetime_pst:
            pst = pytz.timezone("America/Los_Angeles")

            if timezone.is_naive(self.datetime_pst):
                self.datetime_pst = timezone.make_aware(self.datetime_pst, timezone=pytz.UTC)

            self.datetime_pst = self.datetime_pst.astimezone(pst)
        print(f"Saving record with title: {self.title}, datetime_pst: {self.datetime_pst}")
        super().save(*args, **kwargs)

    def get_datetime_in_pst(self):
        pst = pytz.timezone("America/Los_Angeles")
        return self.datetime_pst.astimezone(pst)

    def __str__(self):
        return f"{self.title} - {self.get_datetime_in_pst().strftime('%Y-%m-%d %H:%M:%S %Z')}"