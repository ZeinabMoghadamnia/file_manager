# Generated by Django 4.2.7 on 2024-05-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(blank=True, editable=False, max_length=30, null=True),
        ),
    ]
