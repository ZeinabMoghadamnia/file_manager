from django.db import models
# from ..account.models import User
from applications.account.models import User
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image


class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=30)
    content = models.FileField(upload_to='content/')
    upload_date = models.DateField(auto_now_add=True)
    upload_time = models.TimeField(auto_now_add=True)
    size = models.CharField(max_length=20, editable=False)
    type = models.CharField(max_length=30, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnail/', editable=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_file')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='folder_file')
    
    def create_thumbnail(self):
        if not self.content:
            return

        image_path = os.path.join(settings.MEDIA_ROOT, self.content.name)
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', self.content.name)

        if not os.path.exists(thumbnail_path):
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

        with Image.open(image_path) as img:
            img.thumbnail((100, 100))  
            img.save(thumbnail_path)
    

@receiver(post_save, sender=File)
def update_file_size(sender, instance, created, **kwargs):
    if created and instance.content:
        file_path = instance.content.path
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            instance.size = f"{round(file_size / (1024 * 1024), 2)} MB"
            instance.save()
            
@receiver(post_save, sender=File)         
def create_thumbnail(sender, instance, created, **kwargs):
    if created:
        instance.create_thumbnail()