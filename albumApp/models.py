from django.db import models
from django.contrib.auth.models import User

DEFAULT_IMAGE_PATH = 'media/default.png'


def user_directory_path(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Album(models.Model):
    creator = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, default='')
    artist_name = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=user_directory_path, default=DEFAULT_IMAGE_PATH, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_directory_path, default=DEFAULT_IMAGE_PATH, null=True, blank=True)
