from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    street = models.CharField("street", max_length=255, blank=True)
    city = models.CharField("city", max_length=100, blank=True)
    postal_code = models.CharField("post code", max_length=20, blank=True)
    country = models.CharField("country", max_length=100, blank=True)
    receive_newsletter = models.BooleanField(default=False)
 
    def __str__(self):
        return f"Profil {self.user.username}"
