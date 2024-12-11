from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from creovate.account.models import Profile, UserType


# Register your models here.
@admin.register(Profile)
class CustomUserAdmin(UserAdmin):
    model = Profile


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    model = UserType
