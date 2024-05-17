from django.db import models

# from ..account.models import User
from applications.account.models import User
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
from moviepy.editor import VideoFileClip

class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=20, editable=False)
    
    def calculate_total_size(self):
        total_size = 0
        for folder in self.folder_set.all():
            total_size += folder.calculate_total_size()
        for file in self.folder_file.all():
            # Convert file size from string to integer
            total_size += int(file.size)
        return total_size


@receiver(post_save, sender=Folder)
def update_folder_size(sender, instance, created, update_fields=None, **kwargs):    
    if created or (update_fields and 'size' in update_fields):
        total_size = instance.calculate_total_size()
        # Convert total size to MB and save it as string
        instance.size = f"{total_size} MB"
        instance.save()
        
class File(models.Model):
    name = models.CharField(max_length=30)
    content = models.FileField(upload_to="content/")
    upload_date = models.DateField(auto_now_add=True)
    upload_time = models.TimeField(auto_now_add=True)
    size = models.CharField(max_length=20, editable=False)
    type = models.CharField(max_length=30, editable=False, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to="thumbnail/", editable=False, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_file")
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="folder_file",
    )

    # def create_thumbnail(self):
    #     if not self.content:
    #         return

    #     image_path = os.path.join(settings.MEDIA_ROOT, self.content.name)
    #     thumbnail_path = os.path.join(
    #         settings.MEDIA_ROOT, "thumbnails", self.content.name
    #     )

    #     if not os.path.exists(thumbnail_path):
    #         os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

    #     with Image.open(image_path) as img:
    #         img.thumbnail((100, 100))
    #         img.save(thumbnail_path)

@receiver(post_save, sender=File)
def update_file_type(sender, instance, created, **kwargs):
    if created and not instance.type: 
        _, file_extension = os.path.splitext(instance.content.path)
        print(file_extension)
        if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            instance.type = 'image'
        elif file_extension.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            instance.type = 'video'
        instance.save()
        
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
        if instance.content.name.endswith('.jpg') or instance.content.name.endswith('.jpeg') or instance.content.name.endswith('.png'):
            thumbnail = f"media/thumbnail/{instance.name}.jpg"
            image = Image.open(instance.content)
            image.thumbnail((100, 100))  # ایجاد تامینیل با اندازه دلخواه
            image.save(thumbnail)
            instance.thumbnail = thumbnail
        elif instance.content.name.endswith('.mp4') or instance.content.name.endswith('.MOV'):
            thumbnail = f"media/thumbnail/{instance.name}.jpg"
            # با استفاده از MoviePy یک فریم از ویدیو استخراج می‌کنیم
            video_clip = VideoFileClip(instance.content.path)
            frame = video_clip.get_frame(0)  # استخراج فریم اول از ویدیو
            video_clip.close()  # بستن ویدیو پس از استخراج فریم
            # ذخیره فریم به عنوان تامینیل
            image = Image.fromarray(frame)
            image.thumbnail((100, 100))
            image.save(thumbnail)
            instance.thumbnail = thumbnail
        instance.save()