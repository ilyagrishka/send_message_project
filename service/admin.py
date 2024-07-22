from django.contrib import admin

from service.models import ClientOfService, MailingSettings, MailingMessage


@admin.register(ClientOfService)
class ClientOfServiceAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")
    list_filter = ("full_name",)
    """здесь должен быть ещё owner"""
    search_fields = ("full_name", "email",)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ("status",)
    """здесь должен быть ещё owner"""


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ( "message",)
    """здесь должен быть ещё subject"""

