from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from creovate.account.models import Profile, UserType, Wallet, Order


# Register your models here.
@admin.register(Profile)
class CustomUserAdmin(UserAdmin):
    model = Profile


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    model = UserType


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    model = Wallet


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
