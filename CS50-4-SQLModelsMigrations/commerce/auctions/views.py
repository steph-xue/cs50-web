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
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html",
    {
        "listings": active_listings
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
                "message": "Invalid username and/or password."
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
                "message": "Passwords must match."
            })

        # Attempt to create new user (sees if user already exists), otherwise returns an error message
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
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

    # Gets all comments for the listing item
    listing_comments = Comment.objects.filter(listing_item=listing_data)

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "in_watchlist": in_watchlist,
        "comments": listing_comments
    })


# Allows the user to create a new listing
@login_required(login_url='login')
def create(request):

    # Gets all categories avaliable 
    all_categories = Category.objects.all()

    # POST - allows user to create a new listing via a form
    if request.method == "POST":

        # Get all information provided by the user about the listing
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = float(request.POST["price"])
        category = request.POST["category"]
        owner = request.user

        # If a mandatory field is not filled out, display an error message
        if not title or not description or not price or not category:
            return render(request, "auctions/create.html",
            {
                "message": "Missing information: Please fill out all fields",
                "categories": all_categories
            })

        # Get the category object data
        category_data = Category.objects.get(category_name=category)

        # Returns an error message if the price is not a positive value
        if price <= 0:
            return render(request, "auctions/create.html",
        {
            "message": "Error: Price must be a positive value",
            "categories": all_categories
        })

        # Create listing object
        listing_data = Listing(
            title=title,
            description=description,
            image_url=image_url,
            price=price,
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
            "categories": all_categories
        })
    

# Allows the user to select from different categories to view
def category(request):

    # Gets all categories avaliable 
    all_categories = Category.objects.all()

    # Shows user page to select from all categories avaliable
    return render(request, "auctions/category.html",
        {
            "categories": all_categories
        })


# Allows the user to submit a chosen category and view corresponding listings
def category_listing(request):

    # Gets all categories avaliable 
    all_categories = Category.objects.all()

    # If no category is selected, displays an error message
    if not request.POST.get("category", None):
        return render(request, "auctions/category.html",
        {
            "categories": all_categories,
            "message": "Please select a valid category"
        })
        
    # Retrieves the category selected 
    category = request.POST.get("category", None)
    category_data = Category.objects.get(category_name=category)


    # Retrieves the other categories (others to choose from)
    other_category_data = Category.objects.exclude(category_name=category)

    # Gets all listings within the choosen category
    listings = Listing.objects.filter(category=category_data, is_active=True)

    # Redirects user to view listings in the chose category
    return render(request, "auctions/category_listing.html",
    {
        "categories": other_category_data,
        "listings": listings,
        "category": category_data,
    })


# Allows the user to add a listing to their watchlist
@login_required(login_url='login')
def add_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.add(current_user)

    # Gets all comments for the listing item
    listing_comments = Comment.objects.filter(listing_item=listing_data)

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "watchlist_alert": f"Added {listing_data.title} to {request.user.username}'s watchlist",
        "in_watchlist": True,
        "comments": listing_comments
    })


# Allows the user to remove a listing from their watchlist
@login_required(login_url='login')
def remove_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.remove(current_user)
    
    # Gets all comments for the listing item
    listing_comments = Comment.objects.filter(listing_item=listing_data)

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "watchlist_alert": f"Removed {listing_data.title} from {request.user.username}'s watchlist",
        "in_watchlist": False,
        "comments": listing_comments
    })


# Allows the user to view their watchlist
@login_required(login_url='login')
def watchlist(request):

    # Gets all listings in the current user's watchlist
     current_user = request.user
     watchlist_data = current_user.user_watchlist.all()

    # Displays the user's watchlist 
     return render(request, "auctions/watchlist.html",
    {
        "listings": watchlist_data,
    })

# Allows the user to add a comment
@login_required(login_url='login')
def add_comment(request, id):

    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Get the added comment
    comment = request.POST.get("comment", None)

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Gets all comments for the listing item
    listing_comments = Comment.objects.filter(listing_item=listing_data)

    # Displays error message if no comment added
    if not comment:
        return render(request, "auctions/listing.html",
        {
            "listing": listing_data,
            "in_watchlist": in_watchlist,
            "comments": listing_comments,
            "comment_alert": "No comment was added"
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

