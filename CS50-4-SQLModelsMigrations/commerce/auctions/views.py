from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category, Listing, Comment, Bid

from .models import User


# Allows the user to view the homepage with all active listings
def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html",
    {
        "listings": active_listings
    })


# Allows the user to log in
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Allows the user to log out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Allows the user to register as a new user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

# Allows the user to view a specific auction listing page
def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    return render(request, "auctions/listing.html",
    {
        "listing": listing_data
    })

# Allows the user to create a new listing
def create(request):
    pass
