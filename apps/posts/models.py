from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    date = models.DateField(auto_now=True, editable=False)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Puntuer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuer = models.ManyToManyField(Post)
