from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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


@login_required
def listings(request):
    listings = Listing.objects.all()
    return render(request, "listings.html", {
        "listings": listings,
    })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    return render(request, "listing.html", {
        "listing": listing,
    })


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        try:
            listing = Listing(title=title, description=description, image=image, price=price, seller=request.user)
            listing.save()
        except:
            return render(request, "create.html", {
                "message": "An error happend"
            })
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    return render(request, "create.html")

@login_required
def delete(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id).first()
    if listing.seller == request.user:
        listing.delete()
        return HttpResponseRedirect(reverse("listings"))
    return HttpResponseForbidden("You are not allowed to delete this listing.")

@login_required
def buy(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    if request.user == listing.seller:
        return HttpResponseForbidden("You cant buy ur own thing muther finko")
    if request.method == "POST":
        listing.available = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "buy.html", {
        "id": listing_id,
        "price": listing.price,
        })
    