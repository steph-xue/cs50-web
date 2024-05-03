from django.contrib.auth.models import AbstractUser
from django.db import models


# Model for user database (username, email, password)
class User(AbstractUser):
    pass


# Model for category of auction items database
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name
    

# Model for bid database (bid price, listing item, user who made the bid)
class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user")

    def __str__(self):
        return f"{self.bid} bid made by {self.user}"


# Model for auction listings database (title, description, image url, current price, category, in which users watchlists, owner of the posting)
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=300)
    initial_price = models.FloatField(),
    current_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_category")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_user")

    def __str__(self):
        return self.title
    

# Model for comment database (comment, date and time, listing item, and user who made the comment)
class Comment(models.Model):
    text = models.CharField(max_length=300)
    date_time = models.DateTimeField()
    listing_item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")

    def __str__(self):
        return f"{self.text} commented by {self.user} on {self.listing_item}"



