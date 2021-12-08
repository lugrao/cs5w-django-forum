def parse_posts(all_posts, user):
    posts = []

    for post in all_posts:
        liked = False
        # if user.is_authenticated:
            # liked = bool(post.likes.filter(liked_by=user.id))
        posts.append({
            "id": post.id,
            "author": post.author,
            "title": post.title,
            "content": post.content,
            "timestamp": post.timestamp,
            # "likes": len(post.likes.all()),
            # "liked_by_user": liked,
            "comments": post.comments.all(),
            "comment_number": len(post.comments.all())
        })

    return posts