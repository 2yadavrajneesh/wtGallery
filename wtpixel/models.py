# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='image_user')
    title = models.CharField(max_length=255, blank=False)
    file = models.FileField(upload_to='images', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.title

    @property
    def number_of_liked(self):
        return self.likes.count()


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    file = models.FileField(upload_to='videos', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    file = models.FileField(upload_to='musics', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
