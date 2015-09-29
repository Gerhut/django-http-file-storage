from django.contrib import admin

from models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    list_display_links = None
    list_editable = ('name', 'file')
