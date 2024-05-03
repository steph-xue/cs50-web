from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# Model for user database (username, email, password)
class User(AbstractUser):
    pass


# Model for category of auction items database
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


# Model for auction listings database (title, description, image url, current price, category, in which users watchlists, owner of the posting)
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=300)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_category")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_user")

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    date_time = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")

class Bid(models.Model):
    pass
