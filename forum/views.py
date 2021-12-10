from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

from .models import User, Topic, Post, Follow_User, Follow_Topic
from .util import parse_posts, parse_topics


def index(request):
    all_topics = Topic.objects.all()
    topics = parse_topics(all_topics)
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
    all_posts = topic.posts.all()
    posts = parse_posts(all_posts, request.user)
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

    # Check if authenticated user is a follower
    user_is_follower = None
    if request.user.is_authenticated:
        user_is_follower = bool(Follow_User.objects.filter(
            follower=request.user.id, following=profile_user.id).all())

    # Handle follow and unfollow
    if request.method == "POST":
        try:
            request.POST["follow"]
            new_follow = Follow_User(
                follower=request.user, following=profile_user)
            new_follow.save()
            return HttpResponseRedirect(request.path_info)
        except KeyError:
            pass

        try:
            request.POST["unfollow"]
            follow = Follow_User.objects.get(
                follower=request.user, following=profile_user)
            follow.delete()
            return HttpResponseRedirect(request.path_info)
        except KeyError:
            pass

    topics_following = profile_user.topics_following.all()
    users_following = profile_user.users_following.all()
    return render(request, "forum/profile.html", {
        "profile_user": profile_user,
        "topics_following": topics_following,
        "users_following": users_following,
        "user_is_follower": user_is_follower,

    })


def following_topics(request):
    user = User.objects.get(id=request.user.id)
    topics_following = user.topics_following.all()
    all_posts = Post.objects.filter(
        topic__in=[follow.following for follow in topics_following]).order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)
    return render(request, "forum/following-topics.html", {
        "posts": posts
    })


def following_people(request):
    user = User.objects.get(id=request.user.id)
    users_following = user.users_following.all()
    all_posts = Post.objects.filter(
        author__in=[follow.following for follow in users_following]).order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)
    # print(len(all_posts[0].comments.all()))
    return render(request, "forum/following-people.html", {
        "posts": posts
    })


def all_posts(request):
    all_posts = Post.objects.all()
    posts = parse_posts(all_posts, request.user)
    return render(request, "forum/all-posts.html", {
        "posts": posts
    })


def new_post(request, topic_name):
    # Check if topic exists
    try:
        topic = Topic.objects.get(name=topic_name)
    except Topic.DoesNotExist:
        return render(request, "forum/new-post.html")

    if request.method == "POST":
        if request.user.is_authenticated:
            # Validate form
            title = request.POST["title"]
            if not title or len(title) > 120:
                return render(request, "forum/new-post.html", {
                    "message": "Title must have more than 0 characters and less than 121.",
                    "topic_name": topic_name
                })
            content = request.POST["content"]
            if not content or len(content) > 5000:
                return render(request, "forum/new-post.html", {
                    "message": "Content must have more than 0 characters and less than 5001.",
                    "topic_name": topic_name
                })

            # Save new post
            author = User.objects.get(id=request.user.id)
            new_post = Post(topic=topic, author=author,
                            title=title, content=content)
            new_post.save()
            return HttpResponseRedirect(reverse("topic", kwargs={"topic_name": topic_name}))
        else:
            return render(request, "forum/new-post.html", {
                "message": "You must be logged in to post something.",
                "topic_name": topic_name
            })
    return render(request, "forum/new-post.html", {
        "topic_name": topic_name
    })
