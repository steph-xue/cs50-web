import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Email


# Homepage - directs user to their inbox or to the login screen
def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "mail/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


# Compose - allows the user to submit the compose new email form to send an email (POST only)
@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST (returns error if request method is not POST)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails (returns error if empty)
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users (returns error if recipient user does not exist)
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email (subject and body)
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one email object for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    # If no errors, shows that the email has been sent succesfully (saved in the database)
    return JsonResponse({"message": "Email sent successfully."}, status=201)


# Mailbox - allows the user to view the selected mailbox: inbox, sent, or archive (GET only)
@login_required
def mailbox(request, mailbox):

    # Filter emails returned based on mailbox (returns error if requested mailbox is invalid)
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=False
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order (email json objects)
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)


# Email - allows the user to retrieve an email's detail or update its read/unread or archived/unarchived properties (GET or PUT)
@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email based on the user and email id (returns error if email is not found)
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # GET - Return email contents (in json object format)
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # PUT - Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


# Login - allows the user to login
def login_view(request):

    # POST - Allows the user to submit their login information 
    if request.method == "POST":

        # Retrieves the email and password to try to authenticate the user
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful and then logs the user in
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid email and/or password."
            })
        
    # GET - displays the login form
    else:
        return render(request, "mail/login.html")


# Logout - allows the user to logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register - allows the user to register for a new account
def register(request):

    # POST - Allows the user to submit information to register for a new account
    if request.method == "POST":

        # Retrieves the email (also is the username) details
        email = request.POST["email"]

        # Retrieves the password and confirmation details
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user (returns error if email address (username) is already taken)
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mail/register.html", {
                "message": "Email address already taken."
            })
        
        # Logs in the new user and redirects them to their inbox
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    # GET - displays the registration form
    else:
        return render(request, "mail/register.html")
