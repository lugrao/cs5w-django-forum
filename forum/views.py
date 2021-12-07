from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

from .models import User, Topic, Post


def index(request):
    topics = Topic.objects.all()
    return render(request, "forum/index.html", {
        "topics": topics
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "forum/login.html",
                          {"message": "Invalid username and/or password."})
    else:
        return render(request, "forum/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "forum/register.html",
                          {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "forum/register.html",
                          {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "forum/register.html")


def topic(request, topic_name):
    try:
        topic = Topic.objects.get(name=topic_name)
    except Topic.DoesNotExist:
        return render(request, "forum/topic.html", {
            "message": "This topic doesn't exist."
        })
    posts = topic.posts.all()
    return render(request, "forum/topic.html", {
        "topic": topic,
        "posts": posts
    })


def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, "forum/post.html", {
            "message": "This post doesn't exist."
        })
    comments = post.comments.all()
    return render(request, "forum/post.html", {
        "post": post,
        "comments": comments
    })


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "forum/profile.html", {
            "message": "User non-existent."
        })

    topics_following = profile_user.topics_following.all()
    users_following = profile_user.users_following.all()
    return render(request, "forum/profile.html", {
        "profile_user": profile_user,
        "topics_following": topics_following,
        "users_following": users_following
    })


def following_topics(request):
    return render(request, "forum/following-topics.html")


def following_people(request):
    return render(request, "forum/following-people.html")


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "forum/all-posts.html", {
        "posts": posts
    })