from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("category_listing", views.category_listing, name="category_listing"),
    path("create", views.create, name="create"),
    path("your_listings", views.your_listings, name="your_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("delete_comment/<int:id>", views.delete_comment, name="delete_comment"),
    path("bidlist", views.bidlist, name="bidlist"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("auctions_won", views.auctions_won, name="auctions_won")
]
