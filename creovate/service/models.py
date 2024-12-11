from PIL import Image

from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    freelance = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_image = models.ImageField(default="service_default.jpg", blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.freelance}'


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if self.service_image:
            image = Image.open(self.service_image.path)

            max_height = 500
            max_width = 500

            if image.height > max_height or image.width > max_width:
                output_size = (max_height, max_width)
                image.thumbnail(output_size)
                image.save(self.service_image.path)
