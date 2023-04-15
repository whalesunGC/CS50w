from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='follower')

## Create Posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likecount = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} Posted:'
    class Meta:
        ordering = ("-created_at", "-updated_at")