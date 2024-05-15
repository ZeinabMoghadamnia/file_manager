from django.contrib import admin
# from .models import File, Folder
from applications.storage.models import File, Folder
# Register your models here.

class FileAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'display_thumbnail',)
    
    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return '<img src="{}" style="max-height:100px; max-width:100px;" />'.format(obj.thumbnail.url)
        else:
            return 'No thumbnail available'
    display_thumbnail.allow_tags = True
    display_thumbnail.short_description = 'Thumbnail'

admin.site.register(File, FileAdmin)
admin.site.register(Folder)
