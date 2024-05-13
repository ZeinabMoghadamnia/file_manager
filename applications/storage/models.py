from django.db import models
from ..account.models import User


class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField(max_length=30),
    upload_date = models.DateField(auto_now_add=True)
    upload_time = models.TimeField(auto_now_add=True)
    size = models.DecimalField(max_digits=3, decimal_places=2),
    type = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='thumbnail/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_file')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='folder_file')
