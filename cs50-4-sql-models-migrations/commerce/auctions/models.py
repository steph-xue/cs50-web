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
    

# Model for highest bids database (highest bid price for a listing, user who made the highest bid for a listing)
class Bid(models.Model):
    highest_bid = models.FloatField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_user")

    def __str__(self):
        return f"${self.highest_bid:.2f} bid made by {self.user}"


# Model for auction listings database (each listing includes a title, description, image url, initial price, current highest bid
# category, is active/inactive in the listings, in which users' watchlists, owner of the posting)
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    image_url = models.CharField(max_length=300, default=None)
    initial_price = models.FloatField(default=None)
    current_highest_bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, blank=True, null=True, related_name="listing_bid", default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_category")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_user")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="listing_winner", default=None)

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
    



