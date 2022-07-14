from pdb import post_mortem
from django.db import models
from django.contrib.auth.models import User as UserModel
from django.utils import timezone
from users.models import Profile as ProfileModel


class Post(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.png')
    likes = models.ManyToManyField(UserModel, related_name='like_posts', blank=True)
    published_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
