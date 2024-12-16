from django.contrib import admin

from creovate.service.models import Service, ServiceCategory


admin.site.site_header = "Creovate Admin Panel"
admin.site.site_title = "Creovate Admin"
admin.site.index_title = "Welcome to Creovate Administration"

# Register your models here.
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    model = ServiceCategory

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    model = Service

    # Display fields in the list view
    list_display = ('title', 'category', 'price', 'freelance', 'created_at', 'updated_at')

    # Enable search functionality
    search_fields = ('title',  'category__name')

    # Add filters for quick access
    list_filter = ('category', 'created_at')

    # Read-only fields to prevent accidental changes
    readonly_fields = ('created_at', 'updated_at')

    # Prepopulate slug field based on the title
    prepopulated_fields = {"slug": ("title",)}

    # Customize the admin form layout
    fieldsets = (
        ("Service Details", {
            'fields': ('title', 'description', 'price', 'category', 'freelance', 'service_image')
        }),
        ("Metadata", {
            'fields': ('slug', 'created_at', 'updated_at')
        }),
    )


