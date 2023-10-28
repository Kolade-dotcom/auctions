from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *
from .util import *


class ListingForm(forms.ModelForm):
    class Meta: 
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']


def index(request):
    if request.method == "POST":
        query = request.POST["query"]
        listings = Listing.objects.filter(category=query)
        if listings is not None:
            return render(request, "auctions/index.html", {
                "page_heading": "Active Listings",
                "listings": listings
            })
        
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "page_heading": "Active Listings",
        "listings": listings
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
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


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
        return redirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.current_bid = form.cleaned_data['starting_bid']
            listing.save()
            
            bid = Bid.objects.create(user=request.user, listing=listing, bid_amount=form.cleaned_data['starting_bid'])
            bid.save()
            
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })
    
    
def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    
    highest_bid = Bid.objects.get(bid_amount=listing.current_bid, listing=listing)
    highest_bidder = highest_bid.user
    
    comments = Comment.objects.filter(listing=listing)
    
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "highest_bidder": highest_bidder,
        "comments": comments
    })
    
 
@login_required(login_url='login')
def watch_unwatch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    
    if request.user in listing.watched_by.all():
        listing.watched_by.remove(request.user)
    else:
        listing.watched_by.add(request.user)
    
    return redirect(reverse("listing_page", args=(listing_id,)))
    
    
@login_required(login_url='login')
def bid(request, listing_id):
    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]
        if bid_amount is not None or bid_amount == '':
            return apology(request, "Something went wrong: Try rebiding")
        
        bid_amount = float(bid_amount)
        listing = Listing.objects.get(pk=listing_id)
        
        if bid_amount < listing.current_bid:
            return apology(request, "Sorry, The bid amount must be greater that the current bid")
        
        bid = Bid.objects.create(user=request.user, listing=listing, bid_amount=bid_amount)
        bid.save()
          
        listing.current_bid = bid_amount
        listing.save()
        
        return redirect(reverse("listing_page", args=(listing_id,)))
    return redirect(reverse("listing_page", args=(listing_id,)))


@login_required(login_url='login')
def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    
    highest_bid = Bid.objects.get(bid_amount=listing.current_bid, listing=listing)
    highest_bidder = highest_bid.user
    
    return render(request, "auctions/close_page.html", {
        "winner": highest_bidder
    })
    
    
@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == "POST":
        content = request.POST["content"]
        if content is not None or content == '':
            return apology(request, "Something went wrong: Try retyping comment")
        
        listing = Listing.objects.get(pk=listing_id)
        
        Comment.objects.create(user=request.user, listing=listing, content=content)
        return redirect(reverse("listing_page", args=(listing_id,)))
    return redirect(reverse("listing_page", args=(listing_id,)))


@login_required(login_url='login')
def watchlist(request):
    user = request.user
    watch_listings = user.watchlist.all()
    return render(request, "auctions/index.html", {
        "page_heading": "Watchlist",
        "listings": watch_listings
    })
    
    
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
    

def category_view(request, category_id):
    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/index.html", {
        "page_heading": Category.objects.get(pk=category_id),
        "listings": listings
    })