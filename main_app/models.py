from django.db import models
# Import the User
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.user} "
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.title} posted on {self.date}"
    
    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'post_id': self.id})
    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"{self.text} by {self.user.username} on {self.date}"