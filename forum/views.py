from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Topic, Post, Comment, Follow_User, Follow_Topic, Like_Post, Like_Comment
from .util import parse_comments, parse_posts, parse_topics


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

    all_posts = topic.posts.order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)

    # Check if authenticated user is a follower
    user_is_follower = None
    if request.user.is_authenticated:
        user_is_follower = bool(Follow_Topic.objects.filter(
            follower=request.user.id, following=topic.id).all())

    # Handle follow and unfollow
    if request.method == "POST":
        try:
            request.POST["follow"]
            new_follow = Follow_Topic(
                follower=request.user, following=topic)
            new_follow.save()
            return HttpResponseRedirect(request.path_info)
        except KeyError:
            pass

        try:
            request.POST["unfollow"]
            follow = Follow_Topic.objects.get(
                follower=request.user, following=topic)
            follow.delete()
            return HttpResponseRedirect(request.path_info)
        except KeyError:
            pass

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/topic.html", {
        "topic": topic,
        "posts": posts,
        "user_is_follower": user_is_follower,
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
    })


def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, "forum/post.html", {
            "message": "This post doesn't exist."
        })

    liked_by_user = False
    if request.user.is_authenticated:
        liked_by_user = bool(post.likes.filter(liked_by=request.user.id))

    all_comments = post.comments.all()
    comments = parse_comments(all_comments, request.user)

    # Handle comment post
    if request.method == "POST":
        try:
            comment = request.POST["comment"]
            if len(comment) > 0 and len(comment) < 5001:
                # Save comment
                user = User.objects.get(id=request.user.id)
                post = Post.objects.get(id=post_id)
                new_comment = Comment(post=post, author=user, content=comment,)
                new_comment.save()
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "forum/post.html", {
                    "post": post,
                    "comments": comments,
                    "comment_error": "Comment must have more than 0 characters and less than 5001."
                })
        except KeyError:
            return HttpResponseRedirect(request.path_info)

    return render(request, "forum/post.html", {
        "post": post,
        "likes": len(post.likes.all()),
        "liked_by_user": liked_by_user,
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

    all_posts = profile_user.posts.order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # return render(request, "forum/following-topics.html", {
    #     "page_obj": page_obj,
    #     "pages": list(range(1, paginator.num_pages + 1))
    # })

    return render(request, "forum/profile.html", {
        "profile_user": profile_user,
        "topics_following": topics_following,
        "users_following": users_following,
        "user_is_follower": user_is_follower,
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
    })


def following_topics(request):
    user = User.objects.get(id=request.user.id)
    topics_following = user.topics_following.all()
    all_posts = Post.objects.filter(
        topic__in=[follow.following for follow in topics_following]).order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/following-topics.html", {
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
    })


def following_people(request):
    user = User.objects.get(id=request.user.id)
    users_following = user.users_following.all()
    all_posts = Post.objects.filter(
        author__in=[follow.following for follow in users_following]).order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/following-people.html", {
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
    })


def liked_posts(request):
    user = User.objects.get(id=request.user.id)
    liked_posts = user.liked_posts.order_by("-id").all()
    posts = []
    for like in liked_posts:
        posts.append(like.post)
    posts = parse_posts(posts, request.user)

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/liked-posts.html", {
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
    })


def liked_comments(request):
    user = User.objects.get(id=request.user.id)
    liked_comments = user.liked_comments.order_by("-id").all()
    comments = []
    for like in liked_comments:
        comments.append(like.comment)
    comments = parse_comments(comments, request.user)

    # Paginator
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/liked-comments.html", {
        "page": "liked_comments",
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1)),
        "comments": comments
    })


def all_posts(request):
    all_posts = Post.objects.order_by("-timestamp").all()
    posts = parse_posts(all_posts, request.user)

    # Paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "forum/all-posts.html", {
        "page_obj": page_obj,
        "pages": list(range(1, paginator.num_pages + 1))
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


def edit_post(request, post_id):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id=post_id)
            post.content = request.POST["post-content"]
            if post.author.id == request.user.id:
                if not post.content:
                    return JsonResponse({
                        "error": "Post cannot be empty."
                    }, status=400)
                post.save()
                return JsonResponse({
                    "message": "Post updated."
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Post can only be edited by its author."
                }, status=400)
        except Post.DoesNotExist:
            return JsonResponse({
                "error": "Post not found."
            }, status=404)

    return JsonResponse({
        "error": "User must be authenticated."
    }, status=400)


def delete_post(request, post_id):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id=post_id)
            if post.author.id == request.user.id:
                post.delete()
                return JsonResponse({
                    "message": "Post deleted."
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Post can only be deleted by its author."
                }, status=400)
        except Post.DoesNotExist:
            return JsonResponse({
                "error": "Post not found."
            }, status=404)

    return JsonResponse({
        "error": "User must be authenticated."
    }, status=400)


def like(request, liked):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        liked_object = request.POST["liked_object"]

        # Handle post like
        if liked_object == "post":
            post = Post.objects.get(id=request.POST["id"])
            # Create like
            if liked == "False":
                if not Like_Post.objects.filter(liked_by=user, post=post).exists():
                    like = Like_Post(post=post, liked_by=user)
                    like.save()
                    return JsonResponse({"message": "Like created."}, status=200)
                return JsonResponse({"error": "Like already exists."}, status=400)
            # Delete like
            elif liked == "True":
                try:
                    like = Like_Post.objects.get(liked_by=user, post=post)
                    like.delete()
                except Like_Post.DoesNotExist:
                    return JsonResponse({"message": "Like doesn't exist."}, status=400)
                return JsonResponse({"message": "Like deleted."}, status=200)

        # Handle comment like
        elif liked_object == "comment":
            comment = Comment.objects.get(id=request.POST["id"])
            # Create like
            if liked == "False":
                comment = Comment.objects.get(id=request.POST["id"])
                if not Like_Comment.objects.filter(liked_by=user, comment=comment).exists():
                    like = Like_Comment(comment=comment, liked_by=user)
                    like.save()
                    return JsonResponse({"message": "Like created."}, status=200)
                return JsonResponse({"error": "Like already exists."}, status=400)
            # Delte like
            elif liked == "True":
                try:
                    like = Like_Comment.objects.get(
                        liked_by=user, comment=comment)
                    like.delete()
                except Like_Comment.DoesNotExist:
                    return JsonResponse({"message": "Like doesn't exist."}, status=400)
                return JsonResponse({"message": "Like deleted."}, status=200)

        # Handle bad request
        else:
            return JsonResponse({"error": "Bad request."}, status=400)

    # Handle user not authenticated
    return JsonResponse({"error": "User must be signed in."}, status=400)
