from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post, Follow


# Directs the user to the homepage with all posts
def index(request):

    # Gets all posts ordered in reverse chronological order
    all_posts = Post.objects.all().order_by("id").reverse()

    # Pagination - determines which page to show and only allow maximum 10 posts to be displayed on each page
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    # Directs user to the homepage with all posts ordered in reverse chronological order
    return render(request, "network/index.html", {
        "page_posts": page_posts
    })


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


@login_required
# Allows the user to create a new post
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
        post = Post(
            content = content,
            user = current_user
        )
        post.save()

        # Redirects the user to the homepage with all posts
        return HttpResponseRedirect(reverse("index"))
    
    # GET - Directs the user to the create new post page
    else:
        return render(request, "network/create.html")
    

# Directs the user to a specific user's profile
def profile(request, user_id):

    # Gets all posts of the specific user ordered in reverse chronological order
    profile_user = User.objects.get(pk=user_id)
    user_posts = Post.objects.filter(user=profile_user).order_by("id").reverse()

    # Pagination - determines which page to show and only allow maximum 10 posts to be displayed on each page
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    # Gets all specific user's followers and the people who they are following
    followers = Follow.objects.filter(user_following=profile_user)
    following = Follow.objects.filter(user_follower=profile_user)

    # Determines if the currrent user is following the user's profile
    try:
        if len(followers.filter(user_follower=request.user)) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    # Directs user to the specific user's profile with all posts ordered in reverse chronological order
    return render(request, "network/profile.html", {
        "page_posts": page_posts,
        "profile_user": profile_user,
        "followers": followers,
        "following": following,
        "is_following": is_following
    })


@login_required
# Allows the user to follow the profile
def follow(request):

    # Gets the current user and the profile's user
    current_user = request.user
    profile_user_id = int(request.POST["follow"])
    profile_user = User.objects.get(pk=profile_user_id)

    # Create and save a follow object into the database where the current user follows the profile's user
    follow = Follow(
        user_follower=current_user,
        user_following=profile_user
    )
    follow.save()

    # Redirects the user to the same profile
    user_id = profile_user.id
    return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id}))


@login_required
# Allows the user to unfollow the profile
def unfollow(request):

    # Gets the current user and the profile's user
    current_user = request.user
    profile_user_id = int(request.POST["unfollow"])
    profile_user = User.objects.get(pk=profile_user_id)

    # Delete the follow object from the database so that the current user unfollows the profile's user
    follow = Follow.objects.get(user_follower=current_user, user_following=profile_user)
    follow.delete()

    # Redirects the user to the same profile
    user_id = profile_user.id
    return HttpResponseRedirect(reverse("profile", kwargs={'user_id': user_id}))


@login_required
# Directs the user to the following page to view posts from only users they follow
def following(request):

    # Gets all Follow objects where the user is a follower of another user
    following = Follow.objects.filter(user_follower=request.user)

    # Gets all posts ordered in reverse chronological order
    all_posts = Post.objects.all().order_by("id").reverse()

    # Create an empty list of following posts to add posts to
    following_posts = []

    # Check if the user of the post matches someone the current user is following and add it to the following posts list
    for post in all_posts:
        for follow in following:
            if follow.user_following == post.user:
                following_posts.append(post)

    # Pagination - determines which page to show and only allow maximum 10 posts to be displayed on each page
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    # Directs user to the homepage with all posts ordered in reverse chronological order
    return render(request, "network/following.html", {
        "page_posts": page_posts
    })


@login_required
# Allows the user to edit a post
def edit(request, post_id):

    # POST - Allows user to edit and save the edits to the database
    if request.method == "POST":

        # Gets the json data posted to the backend
        data = json.loads(request.body)

        # Gets the post to edit and saves the edits to the database
        post = Post.objects.get(pk=post_id)
        post.content = data["content"]
        post.save()
        
        # Returns a json response to the use to tell them if the edit was successful
        return JsonResponse({"message": "Edit saved successfully", "data": data["content"]})