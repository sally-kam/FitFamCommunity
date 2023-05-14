from django.db import models
# Import the User
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from storages.backends.s3boto3 import S3Boto3Storage


# Create your models here.
# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     profile = models.OneToOneField('main_app.Profile', on_delete=models.CASCADE, related_name='profile_photo')

#     def __str__(self):
#         return f"Photo for profile_id: {self.profile_id} @{self.url}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    profile_pic = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title} posted on {self.date}"
    
    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'post_id': self.id})
    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) 
    text = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)


    def __str__(self):
        return f"{self.text} from {self.post.title} on {self.date_added}"
    
    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'post_id': self.id})
    
    class Meta:
        ordering = ['-date_added']

