
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path("remove_like/<int:post_id>", views.remove_like, name="remove_like"),
    path("like_status/<int:post_id>", views.like_status, name="like_status"),
    path("like_count/<int:post_id>", views.like_count, name="like_count"),
    path("add_dislike/<int:post_id>", views.add_dislike, name="add_dislike"),
    path("remove_dislike/<int:post_id>", views.remove_dislike, name="remove_dislike"),
    path("dislike_status/<int:post_id>", views.dislike_status, name="dislike_status"),
    path("dislike_count/<int:post_id>", views.dislike_count, name="dislike_count"),
]
