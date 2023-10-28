from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("<int:listing_id>/watch_unwatch", views.watch_unwatch, name="watch_unwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_view, name="category_view")
]
