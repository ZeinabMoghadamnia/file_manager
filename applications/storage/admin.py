from django.contrib import admin
# from .models import File, Folder
from applications.storage.models import File, Folder
# Register your models here.

class FileAdmin(admin.ModelAdmin):
    readonly_fields = ('size',)

admin.site.register(File, FileAdmin)
admin.site.register(Folder)
