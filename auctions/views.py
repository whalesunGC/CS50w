from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm
from .models import Listing, Bid, User


def index(request):
    '''display current active listings. Ordered by date posted.'''
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bid": Bid.objects.all(),
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

def listing_create(request):
    ''' display form to create new listings.'''
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # update auction model with name, category, image_url and bid_start
            form.save()
            return render(request, "auctions/create.html", {
                "form": ListingForm(),
                "status": "Your Listing Is UP!",
            })
        else:
            return render(request, "auctions/create.html", {
                "form":form,
                "status": "Seems like there is something weird with the inputs..."
            })
    return render(request, "auctions/create.html" ,{
        "form": ListingForm(),
    })

def listing_edit(request, pk):
    ''' display form to edit listings.'''
    listing = Listing.objects.get(id=pk)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return render(request, "auctions/edit.html", {
                "form": ListingForm(),
                "status": "Your Listing Is Updated!",
            })
        else:
            return render(request, "auctions/edit.html", {
                "form":form,
                "status": "Seems like there is something weird with the inputs..."
            })
    elif request.method == "GET":
        form = ListingForm(instance=listing)
        return render(request, "auctions/edit.html", {
            "form":form,
        })
    
def listing_delete(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(id=pk)
        listing.delete()
        return HttpResponseRedirect(reverse("index"))

def listing_page(request, pk):
    ''' display selected listing.'''
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=pk),
    })

def listing_filter():
    '''  display all listings filtered by categories. '''
    pass

def user_watchlist():
    '''  display watchlist of logined user. '''
    pass

def admin_interface():
    pass