from django.contrib import admin
from users.models import Owner


@admin.register(Owner)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
