from django.db import models
# from django.utils.translation import gettext_lazy as _

from .managers import CostumeUserManager
# from ..core.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.core.validators import RegexValidator
from django.utils.html import mark_safe


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$',
                                  message=("Please enter the phone number in this format: '09999999999'"))
    phone_number = models.CharField(validators=[mobile_regex], max_length=11, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    groups = models.ManyToManyField(Group, verbose_name='Groups', related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name='User permissions',
                                              related_name='custom_user_set')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']
    objects = CostumeUserManager()


    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    image = models.ImageField(upload_to='users_profile_pics/', null=True, blank=True)

    def img_preview(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="auto" height="100" />' % (self.image))
        else:
            return mark_safe('<img src="static/images/profile.jpg" width="auto" height="100" />')
