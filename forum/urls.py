from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("topic/<str:topic_name>", views.topic, name="topic"),
    path("post/<str:post_id>", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("all-posts", views.all_posts, name="all_posts"),
    path("following/topics", views.following_topics, name="following_topics"),
    path("following/people", views.following_people, name="following_people"),
]
