from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("topic/<str:topic_name>", views.topic, name="topic"),
    path("profile/<str:username>", views.profile, name="profile"),
]
