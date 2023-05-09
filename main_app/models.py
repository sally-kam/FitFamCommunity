from django.db import models
# Import the User
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.CharField(ma)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} posted on {self.date}"
    
    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'post_id': self.id})
    class Meta:
        ordering = ['-date']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
