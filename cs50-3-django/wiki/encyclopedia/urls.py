from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("save_edit", views.save_edit, name="save_edit"),
    path("delete", views.delete, name="delete"),
    path("random", views.randomchoice, name="random")
]
