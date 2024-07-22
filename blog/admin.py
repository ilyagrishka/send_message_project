from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("name", "photo", "created_date", "description")
    list_filter = ('views_counter', 'created_date')
    search_fields = ('name', "description",)
