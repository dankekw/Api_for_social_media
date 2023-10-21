from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/users/create")
def create_user():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.check_email(email):
        return Response(
            json.dumps({"error": "not valid email"}),
            status=201,
            mimetype="application/json",
        )
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.check_user_id(user_id):
        return Response(
            json.dumps({"error": "not user with this id"}),
            status=201,
            mimetype="application/json",
        )
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    post_id = len(POSTS)
    try:
        author_id = int(data["author_id"])
    except ValueError:
        return Response(
            json.dumps({"error": "author id must be a number"}),
            status=201,
            mimetype="application/json",
        )
    text = data["text"]

    if not models.User.check_user_id(author_id):
        return Response(
            json.dumps({"error": "author with this id does not exist"}),
            status=201,
            mimetype="application/json",
        )

    if not models.Post.check_post_text(text):
        return Response(
            json.dumps({"error": "text must be string"}),
            status=201,
            mimetype="application/json",
        )

    post = models.Post(post_id, author_id, text)
    USERS[int(author_id)].posts.append(text)
    POSTS.append(post)
    response = Response(
        json.dumps(
            {
                "id": post.post_id,
                "author_id": post.post_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.check_post_id(post_id):
        return Response(
            json.dumps({"error": "no post with this id"}),
            status=201,
            mimetype="application/json",
        )
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.post_id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
