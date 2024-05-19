from django.db import models

# from ..account.models import User
from applications.account.models import User
import os
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
from moviepy.editor import VideoFileClip


class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subfolders",
    )
    size = models.CharField(max_length=20, editable=False)

    def calculate_total_size(self):
        total_size = 0
        for file in self.folder_file.all():
            total_size += float(file.size.replace(" MB", ""))

        for folder in self.subfolders.all():
            total_size += float(folder.size.replace(" MB", ""))

        return total_size

    def update_size(self):
        total_size = self.calculate_total_size()
        self.size = f"{total_size:.2f} MB"
        self.save()
        if self.parent:
            self.parent.update_size()


@receiver(post_save, sender=Folder)
def update_folder_size(sender, instance, created, update_fields=None, **kwargs):
    if created or (update_fields and "size" in update_fields):
        total_size = instance.calculate_total_size()
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

    def save(self, *args, **kwargs):
        if not self.size:
            self.size = f"{self.content.size / (1024 * 1024):.2f} MB"
        super().save(*args, **kwargs)
        if self.folder:
            self.folder.update_size()


@receiver(post_save, sender=File)
def update_folder_size_on_file_save(sender, instance, **kwargs):
    if instance.folder:
        instance.folder.update_size()


@receiver(post_delete, sender=File)
def update_folder_size_on_file_delete(sender, instance, **kwargs):
    if instance.folder:
        instance.folder.update_size()


@receiver(post_save, sender=File)
def update_file_type(sender, instance, created, **kwargs):
    if created and not instance.type:
        _, file_extension = os.path.splitext(instance.content.path)
        print(file_extension)
        if file_extension.lower() in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
            instance.type = "image"
        elif file_extension.lower() in [".mp4", ".avi", ".mov", ".mkv"]:
            instance.type = "video"
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
        thumbnail_path = f"media/thumbnail/{instance.name}.jpg"

        if instance.content.name.endswith((".jpg", ".jpeg", ".png")):
            image = Image.open(instance.content)
            image.thumbnail((100, 100))

            if image.mode == "RGBA":
                image = image.convert("RGB")

            image.save(thumbnail_path)

        elif instance.content.name.endswith((".mp4", ".MOV")):
            video_clip = VideoFileClip(instance.content.path)
            frame = video_clip.get_frame(0)
            video_clip.close()

            image = Image.fromarray(frame)
            image.thumbnail((100, 100))

            if image.mode == "RGBA":
                image = image.convert("RGB")

            image.save(thumbnail_path)

        instance.thumbnail = thumbnail_path
        instance.save()
