from django.contrib import admin

from .models import User, Topic, Post, Comment, Follow_User, Follow_Topic, Like_Post, Like_Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow_User)
admin.site.register(Follow_Topic)
admin.site.register(Like_Post)
admin.site.register(Like_Comment)
