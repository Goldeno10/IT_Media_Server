from django.contrib import admin
from .models import Media
# Register your models here.


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Admin for media files"""
    list_display = ('id', 'title', 'file', 'uploaded_at', 'file_type', 'owner', 'thumbnail')
    list_filter = ('uploaded_at', 'file_type')
    search_fields = ('title', 'file')
    readonly_fields = ('file_type', 'uploaded_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file')
        }),
        ('Read-only', {
            'fields': ('file_type', 'uploaded_at')
        })
    )