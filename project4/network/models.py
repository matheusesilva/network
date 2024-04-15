from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('User',blank=True, symmetrical=False, related_name="following")
    follow = models.ManyToManyField('User', blank=True, symmetrical=False, related_name="followed_by")
    profile_picture = models.ImageField(upload_to='images',default='images/avatar.webp', blank=True)

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    date_post = models.DateTimeField(auto_now_add=True)
    date_edit_post = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    




