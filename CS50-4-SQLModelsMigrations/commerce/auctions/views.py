from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    
    # Gets the listing item data
    listing_data = Listing.objects.get(pk=id)

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "in_watchlist": in_watchlist,
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
        
    # Retrieves the category selected 
    category = request.POST["category"]
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
        "category": category_data
    })


# Allows the user to add a listing to their watchlist
@login_required(login_url='login')
def add_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.add(current_user)

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "alert": f"Added {listing_data.title} to {request.user.username}'s watchlist",
        "in_watchlist": in_watchlist
    })


# Allows the user to remove a listing from their watchlist
@login_required(login_url='login')
def remove_watchlist(request, id):
    
    # Get the current listing and user
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user

    # Add current user to the watchlist database of the listed item
    listing_data.watchlist.remove(current_user)

    # Determines if the current user has the listing in their watchlist
    in_watchlist = current_user in listing_data.watchlist.all()

    # Redirects user to the listing's page
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data,
        "alert": f"Removed {listing_data.title} to {request.user.username}'s watchlist",
        "in_watchlist": in_watchlist
    })


# Allows the user to view their watchlist
@login_required(login_url='login')
def watchlist(request):
     pass

