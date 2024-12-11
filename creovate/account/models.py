from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image

# Create your models here.

class UserType(models.Model):
    user_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user_type


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_profile = models.ImageField(default="profile_icon.png",null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_profile:
            image = Image.open(self.image_profile.path)

            max_width = 500
            max_height = 500

            if image.height > max_height or image.width > max_width:
                output_size = (max_width, max_height)
                image.thumbnail(output_size)
                image.save(self.image_profile.path)



