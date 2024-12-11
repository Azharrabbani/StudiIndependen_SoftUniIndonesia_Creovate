from django.contrib import admin

from creovate.service.models import Service, ServiceCategory


# Register your models here.
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    model = ServiceCategory


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    prepopulated_fields = {"slug": ("title",)}
