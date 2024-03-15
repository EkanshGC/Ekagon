from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup", views.sign_up, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("listings", views.listings, name="listings"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("buy/<str:listing_id>", views.buy, name="buy"),
    path("delete/<str:listing_id>", views.delete, name="delete"),
    path("search/", views.search, name="search"),
]

