from django.db import models
# Import the User
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.CharField(ma)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} ({self.id}) {self.date}'