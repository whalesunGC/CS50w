from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<TITLE>", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("create_page/", views.new, name="create_page"),
    path("random/", views.random, name='random')
]
