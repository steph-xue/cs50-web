from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} was posted by {self.user.username.capitalize()} on {self.date_time.strftime('%m/%d/%Y, %H:%M:%S')}"
    
class Follow(models.Model):
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")

    def __str__(self):
        return f"{self.user_follower.username.capitalize()} is now following {self.user_following.username.capitalize()}"