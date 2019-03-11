from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class Story(models.Model):
    title = models.CharField(max_length=500)
    story = models.CharField(max_length=5000)
    date = models.DateField(auto_now=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[0:40]


class Stydno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class NeStydno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Proud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
