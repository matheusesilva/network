
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-post",views.addpost, name="add"),
    path("user<int:user>", views.user_page, name="user_page"),
    path("user<int:user>/folowing", views.following, name="following"),
    path("post<int:post>/edit", views.edit, name="edit"),
    path("post<int:post>/like", views.like, name="like"),
    path("user<int:user>/folow", views.follow, name="follow")
]
