from django.contrib import admin
from .models import SongModel


class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'audio_file', 'created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(SongModel, SongAdmin)
