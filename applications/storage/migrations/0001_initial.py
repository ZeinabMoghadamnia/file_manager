# Generated by Django 4.2.7 on 2024-05-15 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('content', models.FileField(upload_to='content/')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('upload_time', models.TimeField(auto_now_add=True)),
                ('size', models.CharField(editable=False, max_length=20)),
                ('type', models.CharField(blank=True, max_length=30, null=True)),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='thumbnail/')),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_file', to='storage.folder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_file', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
