from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser
from django.utils import timezone

@receiver(pre_save, sender=CustomUser)
def update_updated_at(sender, instance, **kwargs):
    instance.updated_at = timezone.now()