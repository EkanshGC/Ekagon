from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout


from .models import User, Listing


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
        
        return HttpResponseRedirect(reverse('index'))


    return render(request, "login.html")


def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        email = request.POST["email"]
        print('asdhuashd')

        if password == password_confirm:
            print('pass wo')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def listings(request):
    listings = Listing.objects.all()
    return render(request, "listings.html", {
        "listings": listings,
    })

def listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    return render(request, "listing.html", {
        "listing": listing,
    })