from django.db import models
# from ..account.models import User
from applications.account.models import User
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=30)
    content = models.FileField(upload_to='content/')
    upload_date = models.DateField(auto_now_add=True)
    upload_time = models.TimeField(auto_now_add=True)
    size = models.CharField(max_length=20, editable=False)
    type = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='thumbnail/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_file')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='folder_file')

@receiver(post_save, sender=File)
def update_file_size(sender, instance, created, **kwargs):
    if created and instance.content:  # Check if the instance is newly created and has content
        file_path = instance.content.path
        if os.path.exists(file_path):  # Check if the file exists
            file_size = os.path.getsize(file_path)
            instance.size = f"{round(file_size / (1024 * 1024), 2)} MB"
            instance.save()  # Save the instance with the updated size
