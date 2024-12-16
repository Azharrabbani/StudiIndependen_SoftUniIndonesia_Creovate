from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from creovate.account.models import Profile, UserType, Wallet, Order

admin.site.site_header = "Creovate Admin Panel"
admin.site.site_title = "Creovate Admin"
admin.site.index_title = "Welcome to Creovate Administration"

# Register your models here.
@admin.register(Profile)
class CustomUserAdmin(UserAdmin):
    model = Profile
    list_display = ('email', 'username', 'user_type', 'created_at', 'updated_at', 'image_preview')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'image_profile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('user_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'image_profile'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image_profile:
            return f'<img src="{obj.image_profile.url}" style="width: 50px; height: 50px; object-fit: cover;">'
        return "No Image"

    image_preview.allow_tags = True
    image_preview.short_description = "Image Preview"


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    model = UserType
    search_fields = ('user_type',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    model = Wallet

    list_display = ('profile', 'balance', 'updated_at')
    search_fields = ('profile__username', 'profile__email')
    list_filter = ('updated_at',)
    readonly_fields = ('updated_at',)

    fieldsets = (
        ("Wallet Information", {
            'fields': ('profile', 'balance')
        }),
        ("Timestamps", {
            'fields': ('updated_at',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order

    list_display = ('id', 'order_date',)
    search_fields = ('id',)
    list_filter = ('order_date',)
    readonly_fields = ('id', 'order_date')

