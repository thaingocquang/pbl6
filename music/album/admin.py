from django.contrib import admin
from .models import AlbumModel


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(AlbumModel, AlbumAdmin)
