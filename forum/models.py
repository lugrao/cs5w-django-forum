from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Topic:
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topics")
    name = models.TextField(max_length=120)
    description = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Topic: "{self.name}". Creator: {self.creator.username}.'


class Post:
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    title = models.TextField(max_length=120)
    content = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post: "{self.title}". Author: {self.author.username}. Topic: "{self.topic.name}".'


class Comment:
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment in "{self.post.title}". Author: {self.author.username}.'


class Follow_User:
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Follow_Topic:
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f'{self.follower.username} follows "{self.following.name}"'


class Like_Post:
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")
    liked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'{self.liked_by.username} likes post "{self.post.title}".'


class Like_Comment:
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes")
    liked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'{self.liked_by.username} likes comment in post "{self.comment.post.title}".'
