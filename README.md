# CS50W Final Project: Forum

## Project Description

This project is an internet forum inspired by the old internet forums, and also by Reddit. The main page shows the topics created by users. Inside each topic, users can create posts, and inside each post they can create comments. Each topic and each user can be followed or unfollowed, and each post and comment can be liked or unliked. It's not mandatory to create an account; topics, posts, comments and user profiles can be viewed without being logged in.

## Distinctiveness and Complexity

**Final Project: Forum** has similarities with **Project 4: Network**. Both projects have users, posts, and the posibility to follow/unfollow users and like/unlike posts. What makes **Forum** different from **Network** is the focus on topics and posts instead of users. What makes it more complex is the addition of topics, which can be created, followed and unfollowed, and comments, which can be posted, liked or unliked.

In terms of navigation features, both **Forum** and **Network** have a user's profile page for each user, a page showing all the posts that's been published, and a page showing posts from people they follow. In **Forum** there's also a page showing all the topics that's been created, a page showing posts from topics followed by the user, a page showing posts liked by the user, and a page showing comments liked by the user. In both **Network** and **Forum**, each post has a link to the author's profile, a heart emoji indicating wether the post has been liked or not, and a number below the heart emoji indicating the amount of likes. In **Forum**, each post also links to the topic it belongs to and the comments it has.

In terms of overall complexity, **Forum** exceeds **Network** in the number of models created (8 v. 4), the number of views and url paths (17 v. 8), and the number of files created (30 v. 13).

## Files created

### `views.py`

This file contains the views for the entire project.

Functions:

- `index`: Renders `index.html` with all the topics that were created.

- `login_view`: Renders `login.html` and lets the user log in, asking for her username and password.

- `logout_view`: Logs out the user and renders `index.html`.

- `register`: Renders `register.html` and lets the user register, asking him for a username, a password and an email. Saves the new user data into the database.

- `topic`: Renders `topic.html` and shows the selected topic with all its posts. Allows user to follow or unfollow the topic.

- `post`: Show selected post with all its comments. Allows user to like and unlike the post and the comments. Allows user to post comments.

- `profile`: Renders `profile.html` and shows the selected profile. Allows the user to follow or unfollow the profile. Shows which topics and users are being followed by the profile owner. Shows posts posted by the profile's owner.

- `following_topics`: Renders `following-topics.html` and shows posts from topics the user follows.

- `following_people`: Renders `following-people.html` and shows posts from people the user follows.

- `liked_posts`: Renders `liked-posts.html` and shows all posts liked by the user.

- `liked_comments`: Renders `liked-comments.html` and shows all comments liked by the user.

- `all_posts`: Renders `all-posts.html` and shows all posts from all topics.

- `new_topic`: Renders `new-topic.html`, showing a form that allows the user to create a new topic. Saves the new topic into the database and redirects to that topic's page.

- `new_post`: Renders `new-post.html`, showing a form that allows the user to create a new post. Saves the new post into the database and redirects to the topic's page.

- `edit_post`: Saves the new version of an existing post, modified by the user.

- `delete_post`: Deletes the selected post.

- `like`: Handles likes for comments and posts, saving them into the database or deleting them.

### `util.py`

Helper file to parse topics, posts and comments.

Each function (`parse_topics`, `parse_posts`, and `parse_comments`) recieves a list of items and returns a new list with the same data plus some additional data needed by the templates.

### `models.py`

Models:

- `User`: defines a User with the default fields given by Django.

- `Topic`: defines a Topic with the following fields:

  - `creator` (User model as a foreign key)
  - `name` (text field)
  - `description` (tex field)
  - `timestamp`

- `Post`: defines a Post with the following fields:

  - `topic` (Topic model as a foreign key)
  - `author` (User model as a foreign key)
  - `title` (text field)
  - `content` (text field)
  - `timestamp`

- `Comment`: defines a Comment with the following fields:

  - `post` (Post model as a foreign key)
  - `author` (User as a foreign key)
  - `content` (text field)
  - `timestamp`

- `Fllow_User`: defines a User Follow with the following fields:

  - `follower` (User as a foreign key)
  - `following` (User as a foreign key)

- `Follow_Topic`: defines a Topic Follow with the following fields:

  - `follower` (User as a foreign key)
  - `following` (Topic as a foreign key)

- `Like_Post`: defines a Post Like with the following fields:
  - `comment` (Comment as a foreign key)
  - `liked_by` (User as a foreign key)

### `urls.py`

Paths:

- `index` shows the home page.

- `login` shows the login page. When user logs in, redirects to `index`.

- `logout` logs out the user and redirects to `index`.

- `register` shows register page. When user registers, redirects to `index`.

- `topic` shows the topics page. Receives a topic name as an argument.

- `post` shows the post page. Receives a post ID as an argument.

- `profile` shows the profile page. Receives a username as an argument.

- `all_posts` shows a page with all the posts that has been published.

- `following_topics` shows a page of all the topics that a logged in user is following.

- `following_people` shows a page of all the users that a logged in user is following.

- `liked_posts` shows a page with all the posts a logged in user has liked.

- `liked_comments` shows a page with all the comments a logged in user has liked.

- `new_topic` shows the new topic page. When a new topic is created, redirects to that topic's page.

- `new_post` shows the new post page. Receives a post ID as an argument. When a post is submitted, redirects to the topic page.

- `edit_post` sends a request to the database for editing a post. Receives a post ID as an argument.

- `delete_post` sends a request to the database for deleting a post. Receives a post ID as an argument.

- `like` sends a request to the database for liking or unliking posts or comments. Receives the strings 'True' or 'False' as arguments.

### Templates

- `layout.html` shows the title of the page and the navbar. This view is shown in all pages.

- `posts.html` shows a list of posts. Each post can be liked and unliked, edited and deleted. This template is used by other templates that show posts.

- `comments.html` shows a list of comments. Each comment can be liked and unliked. This template is used by other templates that show comments.

- `index.html` shows all topics.

- `all-posts.html` shows all posts from all topics. Uses `posts.html`.

- `following-people.html` shows posts from people followed by the user. Uses `posts.html`.

- `following-topics.html` shows posts from topics followed by the user. Uses `posts.html`.

- `liked-comments.html` shows comments liked by the user. Uses `comments.html`.

- `liked-posts.html` shows posts liked by the user. Uses `posts.html`.

- `login.html` shows the login view.

- `new-post.html` shows the form to post a new post.

- `new-topic.html` shows the form to create a new topic.

- `post.html` shows a post with its comments. Uses `comments.html`.

- `profile.html` shows a user's profile, with a list of topics and people being followed by the profile's owner. Shows posts from the profile's owner. Uses `posts.html`.

- `register.html` shows the register form.

- `topic.html` shows all posts from a topic. Uses `posts.html`.

### Static files

- `comments.css`: styles for `comments.html`.

- `editDeletPost.js`: JavaScript for editing and deleting posts. When the `Edit` button is clicked, a textarea appears with the current text in it. When saving the changes, an edit-post request is sent to the database, then the textarea gets hidden via CSS and the edited post shows the modified text. When the `Delete` button is clicked, a delete-post request is sent to the database and the post dissapears via CSS.

- `following.css`: styles for `following-people.html` and `following-topics.html`.

- `form.css`: styles for the forms in `login.html`, `new-post.html`, `post.html` and `register.html`.

- `index.css`: styles for `index.html`.

- `layout.css`: styles for `layout.html`.

- `like.js`: JavaScript for liking and unliking posts and comments. It shows a white heart if the post is not liked by the user, and a red heart if the post is liked. In both cases, a request is sent to the database to update the like status.

- `post.css`: styles for `post.html`.

- `profile.css`: styles for `profile.html`.

- `topic.css`: styles for `topic.html`.

## How to run the application

Install Django.

Go to the root folder of the project.

Run the following commands to setup the database:

```
$ python manage.py makemigrations forum
$ python manage.py migrate
```

Start the development server:

```
python manage.py runserver
```
