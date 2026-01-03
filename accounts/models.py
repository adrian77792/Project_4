from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from colorfield.fields import ColorField
 
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
    
class ThemeSettings(models.Model):
    background_default_color = ColorField(default="#F7F0DB")
    text_default_color = ColorField(default="#1E180D")
    action_primary_default_color = ColorField(default="#BF4630")
    action_secondary_default_color = ColorField(default="#5A83A6")

    class Meta:
        verbose_name = "Theme settings"

    def str(self):
        return "Theme settings"