from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


# Directs the user to the homepage with all posts
def index(request):
    return render(request, "network/index.html")


# Logs the user in
def login_view(request):

    # POST - Allows user to submit login information
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Checks if authentication successful and redirects the user to the homepage
        # Returns an error message if invalid username/password
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
        
    # GET - Directs the user to the login page
    else:
        return render(request, "network/login.html")


# Logs the user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Allows the user to register for a new account
def register(request):

    # POST - Allows user to submit information to register for a new account
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and redirects the user to the homepage
        # Returns an error message if the username is already taken
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    # GET - Directs the user to the register page
    else:
        return render(request, "network/register.html")


def create(request):

    # POST - Allows the user to submit new post information
    if request.method == "POST":

        # Gets the content and user who posted
        current_user = request.user
        content = request.POST["content"]

        # Checks to make sure the content field is not empty
        if content == "":
            return render(request, "network/create.html", {
                "message": "Content field cannot be empty."
            })

        # Creates a new post and save it in the database
        post = POST.objects.create_post(
            content = content,
            user = current_user
        )
        post.save()

        # Redirects the user to the homepage with all posts
        return HttpResponseRedirect(reverse("index"))
    
    # GET - Directs the user to the create new post page
    else:
        return render(request, "network/create.html")