# Generated by Django 4.2.5 on 2023-09-18 09:45

import albumApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albumApp', '0002_alter_album_options_alter_album_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='slug',
        ),
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(blank=True, default='media/default.png', null=True, upload_to=albumApp.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='albumimage',
            name='image',
            field=models.ImageField(blank=True, default='media/default.png', null=True, upload_to=albumApp.models.user_directory_path),
        ),
    ]