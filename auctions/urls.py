from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.listing_create, name="create"),
    path("edit/<pk>", views.listing_edit, name="edit"),
    path("delete/<pk>", views.listing_delete, name="delete"),
    path("close/<pk>", views.listing_close, name="close"),
    path("listing/<pk>", views.listing_page, name="listing"),
    path("filter/", views.listing_filter, name="filter"),
    path("watchlist/<pk>", views.user_watchlist, name="watchlist"),
]
