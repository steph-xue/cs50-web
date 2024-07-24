from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import User, Category, Listing, Comment, Bid


# Allows the user to view the homepage with all active listings
def index(request):

    # Gets all active listings (sorted by alphabetical order by title)
    active_listings = Listing.objects.filter(is_active=True)
    sorted_active_listings = sorted(active_listings, key=lambda listing: listing.title)

    # Renders the homepage with all active listings
    return render(request, "auctions/index.html",
    {
        "listings": sorted_active_listings
    })


# Allows the user to log in
def login_view(request):

    # POST - allows the user to login via a form
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        # If successful, redirects to the homepage, otherwise displays an error message
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message_red_alert": "Invalid username and/or password."
            })
    # GET - displays the login page
    else:
        return render(request, "auctions/login.html")


# Allows the user to log out
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Allows the user to register as a new user
def register(request):

    # POST - allows user to register via a form
    if request.method == "POST":

        # Gets all information about the new user
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation, otherwise returns an error message
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message_red_alert": "Passwords must match."
            })

        # Attempt to create new user (sees if user already exists), otherwise returns an error message
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message_red_alert": "Username already taken."
            })
        
        # Logs the user in and redirects them to the homepage
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    # GET - displays the register new user page
    else:
        return render(request, "auctions/register.html")
    

# Allows the user to view a specific auction listing page
def listing(request, id):

    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Gets all comments for the listing item (sorted in reverse chronological order by date/time)
    listing_comments = Comment.objects.filter(listing_item=listing_data)
    sorted_listing_comments = sorted(listing_comments, key=lambda comment: comment.date_time)

    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "in_watchlist": in_watchlist,
        "comments": sorted_listing_comments
    })
    

# Allows the user to select from different categories to view
def category(request):

    # Gets all categories avaliable (sorted in alphabetical order by category name)
    all_categories = Category.objects.all()
    sorted_all_categories = sorted(all_categories, key=lambda category: category.category_name)

    # Shows user page to select from all categories avaliable
    return render(request, "auctions/category.html",
        {
            "categories": sorted_all_categories
        })


# Allows the user to submit a chosen category and view corresponding listings
def category_listing(request):

    # Gets all categories avaliable (sorted in alphabetical order by category name)
    all_categories = Category.objects.all()
    sorted_all_categories = sorted(all_categories, key=lambda category: category.category_name)

    # If no category is selected, displays an error message
    if not request.POST.get("category", None):
        return render(request, "auctions/category.html",
        {
            "categories": sorted_all_categories,
            "message_red_alert": "Please select a valid category"
        })
    
    # Retrieves the category selected 
    category = request.POST.get("category", None)
    category_data = Category.objects.get(category_name=category)

    # Retrieves the other categories to choose from (sorted in alphabetical order by category name)
    other_category_data = Category.objects.exclude(category_name=category)
    sorted_other_category_data = sorted(other_category_data, key=lambda category: category.category_name)

    # Gets all listings within the choosen category (sorted in alphabetical order by title)
    active_listings = Listing.objects.filter(category=category_data, is_active=True)
    sorted_active_listings = sorted(active_listings, key=lambda listing: listing.title)

    # Redirects user to view listings in the chose category
    return render(request, "auctions/category_listing.html",
    {
        "categories": sorted_other_category_data,
        "category": category_data,
        "listings": sorted_active_listings,
    })


# Allows the user to create a new listing
@login_required(login_url='login')
def create(request):

    # Gets all categories avaliable (sorted in alphabetical order by category name)
    all_categories = Category.objects.all()
    sorted_all_categories = sorted(all_categories, key=lambda category: category.category_name)

    # POST - allows user to create a new listing via a form
    if request.method == "POST":

        # Get all information provided by the user about the listing
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        initial_price = float(request.POST["initial_price"])
        category = request.POST["category"]
        owner = request.user

        # If a mandatory field is not filled out, display an error message
        if not title or not description or not initial_price or not category:
            return render(request, "auctions/create.html",
            {
                "categories": sorted_all_categories,
                "message_red_alert": "Missing information: Please fill out all fields"
            })

        # Returns an error message if the price is not a positive value
        if initial_price <= 0:
            return render(request, "auctions/create.html",
        {
            "categories": all_categories,
            "message_red_alert": "Error: Price must be a positive value"
        })

        # Get the category object data
        category_data = Category.objects.get(category_name=category)

        # Create listing object
        listing_data = Listing(
            title=title,
            description=description,
            image_url=image_url,
            initial_price=initial_price,
            category=category_data,
            owner=owner
        )

        # Save listing object to the database
        listing_data.save()
        
        # Redirects user to the new listing's page
        return HttpResponseRedirect(reverse("listing", args=(listing_data.id,)))

    # GET - displays the page to create a new listing
    else:
        return render(request, "auctions/create.html",
        {
            "categories": sorted_all_categories
        })


# Allows the user to view their own listed auctions
@login_required(login_url='login')
def your_listings(request):

    # POST - Allows the user to select from viewing all, only active, or only inactive listings owned by the user
    if request.method == "POST":

        # Gets the listing type selected by the user (all, active, or inactive)
        current_user = request.user
        listing_type = request.POST["listing_type"]

        if listing_type == "active":
            owner_listings = current_user.listing_user.filter(is_active=True)
        elif listing_type == "inactive":
            owner_listings = current_user.listing_user.filter(is_active=False)
        else:
            owner_listings = current_user.listing_user.all()

        # Sort the user's own listings (in alphabetical order by title)
        sorted_owner_listings = sorted(owner_listings, key=lambda listing: listing.title)

        # Displays the user's own listings 
        return render(request, "auctions/your_listings.html",
        {
            "listings": sorted_owner_listings,
            "listing_type": listing_type
        })

    # GET - displays all of the user's own listed auctions by default (active and inactive)
    else:

        # Gets all listings owned by the user (sorted in alphabetical order by title)
        current_user = request.user
        owner_listings = current_user.listing_user.all()
        sorted_owner_listings = sorted(owner_listings, key=lambda listing: listing.title)

        # Displays the user's listings 
        return render(request, "auctions/your_listings.html",
        {
            "listings": sorted_owner_listings
        })


# Allows the user to view their watchlist
@login_required(login_url='login')
def watchlist(request):

    # Gets all active listings in the current user's watchlist (sorted in alphabetical order by title)
     current_user = request.user
     watchlist_data = current_user.user_watchlist.filter(is_active=True)
     sorted_watchlist_data = sorted(watchlist_data, key=lambda listing: listing.title)

    # Displays the user's watchlist 
     return render(request, "auctions/watchlist.html",
    {
        "listings": sorted_watchlist_data
    })


# Allows the user to add a listing to their watchlist
@login_required(login_url='login')
def add_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.add(current_user)

    # Gets all comments for the listing item (sorted in reverse chronological order by date/time)
    listing_comments = Comment.objects.filter(listing_item=listing_data)
    sorted_listing_comments = sorted(listing_comments, key=lambda comment: comment.date_time)

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "in_watchlist": True,
        "comments": sorted_listing_comments,
        "message_green_alert": f"Added {listing_data.title} to {request.user.username.capitalize()}'s watchlist"
    })


# Allows the user to remove a listing from their watchlist
@login_required(login_url='login')
def remove_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Remove current user to the watchlist database of the listed item
    listing_data.watchlist.remove(current_user)
    
    # Gets all comments for the listing item (sorted in reverse chronological order by date/time)
    listing_comments = Comment.objects.filter(listing_item=listing_data)
    sorted_listing_comments = sorted(listing_comments, key=lambda comment: comment.date_time)

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "in_watchlist": False,
        "comments": sorted_listing_comments,
        "message_green_alert": f"Removed {listing_data.title} from {request.user.username.capitalize()}'s watchlist"
    })


# Allows the user to add a comment
@login_required(login_url='login')
def add_comment(request, id):

    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Gets all comments for the listing item (sorted in reverse chronological order by date/time)
    listing_comments = Comment.objects.filter(listing_item=listing_data)
    sorted_listing_comments = sorted(listing_comments, key=lambda comment: comment.date_time)

    # Get the added comment
    comment = request.POST.get("comment", None)

    # Displays error message if no comment added
    if not comment:
        return render(request, "auctions/listing.html",
        {
            "listing": listing_data,
            "in_watchlist": in_watchlist,
            "comments": sorted_listing_comments,
            "message_red_alert": "Error: No comment was added"
        })

    # Get the date and time the comment was added
    date_time=datetime.datetime.now()

    # Create a new comment object for the listing item
    new_comment = Comment(
        text=comment,
        date_time=date_time,
        listing_item=listing_data,
        user=current_user
    )

    # Save the comment into the database
    new_comment.save()

    # Redirects user back to the listing's page
    return HttpResponseRedirect(reverse("listing", args=(id,)))


# Allows the user to delete their own comments
@login_required(login_url='login')
def delete_comment(request, id):

    # Get the selected comment
    comment_id = request.POST["delete_comment"]
    comment_data = Comment.objects.get(pk=comment_id)

    # Delete the selected comment
    comment_data.delete()

    # Redirects user back to the listing's page
    return HttpResponseRedirect(reverse("listing", args=(id,)))


# Allows the user to view their bidding list (listings where they hold the highest bid)
@login_required(login_url='login')
def bidlist(request):
     
    # Gets all bids that the current user's holds the highest bid for
    current_user = request.user
    bidlist_data = current_user.bid_user.all()

    # Create a new list to store all bid listings 
    bid_list = []

    # Iterates through all highest bids the user holds and appends the associated listings to the bid_list
    for bid in bidlist_data:
         listing = Listing.objects.get(current_highest_bid=bid)
         bid_list.append(listing)
    
    # Sort the highest biding list (in alphabetical order by title of listing)
    sorted_bid_list = sorted(bid_list, key=lambda listing: listing.title)

    # Displays the user's highest bidding list
    return render(request, "auctions/bidlist.html",
    {
        "listings": sorted_bid_list,
    })


# Allows the user to add bid for a listing
@login_required(login_url='login')
def add_bid(request, id):

    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Gets all comments for the listing item (sorted in reverse chronological order by date/time)
    listing_comments = Comment.objects.filter(listing_item=listing_data)
    sorted_listing_comments = sorted(listing_comments, key=lambda comment: comment.date_time)

    # Get the added bid amount
    bid = request.POST.get("bid", None)

    # Displays error message if no bid was added
    if not bid:
        return render(request, "auctions/listing.html",
        {
            "listing": listing_data,
            "in_watchlist": in_watchlist,
            "comments": sorted_listing_comments,
            "message_red_alert": "Error: No bid was added"
        })

    # Convert bid to float (once checked if bid was actually added)
    bid = float(bid)

    # Check to see if a current highest bid exists for the listing
    if listing_data.current_highest_bid:

        # Return an error if the bid is lower than or equal to the current highest bidding price
        if bid <= listing_data.current_highest_bid.highest_bid:
            return render(request, "auctions/listing.html",
            {
                "listing": listing_data,
                "in_watchlist": in_watchlist,
                "comments": listing_comments,
                "message_red_alert": "Error: Bid is lower than or equal to that of the current highest bidding price"
            })
        
        # Delete the old highest bid from the database
        old_id = listing_data.current_highest_bid.id
        old_bid = Bid.objects.get(pk=old_id)
        old_bid.delete()
        
    # If no bid exists for the listing, return an error if the bid is lower than the starting price
    else:
        if bid < listing_data.initial_price:
            return render(request, "auctions/listing.html",
            {
                "listing": listing_data,
                "in_watchlist": in_watchlist,
                "comments": listing_comments,
                "message_red_alert": "Error: Bid is lower than the starting price"
            })
    
    # Create a new highest bid object
    new_highest_bid = Bid(
        highest_bid=bid,
        user=current_user
    )

    # Save the new highest bid into the database
    new_highest_bid.save()

    # Add the newly added highest bid to the listing's highest bid field
    listing_data.current_highest_bid = new_highest_bid
    listing_data.save()

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.add(current_user)

    # Redirects user back to the listing's page with a success message
    return render(request, "auctions/listing.html",
        {
            "listing": listing_data,
            "in_watchlist": True,
            "comments": sorted_listing_comments,
            "message_green_alert": f"Bid of ${bid:.2f} was added successfully! Listing is also added to your the watchlist!"
        })

# Allows the user to close a listing if they are the owner of the listing
@login_required(login_url='login')
def close_listing(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    
    # Closes the current listing if the user is the owner of the listing and sets its winner
    if current_user == listing_data.owner:
        listing_data.is_active = False
        if listing_data.current_highest_bid:
            listing_data.winner = listing_data.current_highest_bid.user
        else:
            listing_data.winner = None
    
    # Saves the winner of the listing
    listing_data.save()

    # Gets all remaining active listings (sorted by alphabetical order by title)
    active_listings = Listing.objects.filter(is_active=True)
    sorted_active_listings = sorted(active_listings, key=lambda listing: listing.title)

    # Redirects user to the homepage of active listings
    return render(request, "auctions/index.html",
        {
            "listings": sorted_active_listings,
            "message_green_alert": f"Congratulations! Your listing for {listing_data.title} has been closed successfully!"
        })


# Allows the user to see the bidding auctions they have won (after the listing has been closed)
@login_required(login_url='login')
def auctions_won(request):
     
    # Gets all listings the current user has won (sorted in alphabetical order by title)
    current_user = request.user
    winner_listings = current_user.listing_winner.all()
    sorted_winner_listings = sorted(winner_listings, key=lambda listing: listing.title)

    # Displays the bidding auctions the user has won
    return render(request, "auctions/auctions_won.html",
    {
        "listings": sorted_winner_listings
    })


