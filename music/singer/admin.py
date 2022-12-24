from django.contrib import admin
from .models import SingerModel
from django.utils.html import mark_safe


class SingerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'created_at', 'updated_at']
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        return obj.avatar_preview

    avatar_preview.short_description = 'Avatar preview'
    avatar_preview.allow_tags = True


admin.site.register(SingerModel, SingerAdmin)
