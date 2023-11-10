from app import app, USERS, POSTS, models
from flask import request, Response, url_for
from http import HTTPStatus
from matplotlib import pyplot as plt
import json


@app.post("/users/create")
def create_user():
    data = request.get_json()
    user_id = len(USERS)
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
    except KeyError:
        return Response(
            json.dumps({"error": "not all parameters are received"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if not models.User.check_email(email) or not all(
        user.email != email for user in USERS
    ):
        return Response(
            json.dumps({"error": "not valid email"}),
            status=HTTPStatus.BAD_REQUEST,
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
                "posts": [get_post(post.post_id).get_json() for post in user.posts],
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
            json.dumps({"error": "not user with such id"}),
            status=HTTPStatus.BAD_REQUEST,
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
                "posts": [get_post(post.post_id).get_json() for post in user.posts],
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
        try:
            author_id = int(data["author_id"])
        except ValueError:
            return Response(
                json.dumps({"error": "author id must be a number"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
        text = data["text"]
    except KeyError:
        return Response(
            json.dumps({"error": "not user with such id"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if not models.User.check_user_id(author_id):
        return Response(
            json.dumps({"error": "author with this id does not exist"}),
            status=201,
            mimetype="application/json",
        )

    if not models.Post.check_post_text(text):
        return Response(
            json.dumps({"error": "text must be string"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    post = models.Post(post_id, author_id, text)
    USERS[author_id].posts.append(post)
    POSTS.append(post)

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


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.check_post_id(post_id):
        return Response(
            json.dumps({"error": "no post with this id"}),
            status=HTTPStatus.BAD_REQUEST,
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


@app.post("/posts/<int:post_id>/reaction")
def set_reaction(post_id):
    if not models.Post.check_post_id(post_id):
        return Response(
            json.dumps({"error": "no post with such id"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    post = POSTS[post_id]
    data = request.get_json()
    try:
        try:
            user_id = int(data["user_id"])
        except ValueError:
            return Response(
                json.dumps({"error": "author id must be a number"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )

        if not models.User.check_user_id(user_id):
            return Response(
                json.dumps({"error": "author with such id not found"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
        reaction = data["reaction"]
    except KeyError:
        return Response(
            json.dumps({"error": "not user with such id"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    USERS[user_id].total_reactions += 1
    post.reactions.append(reaction)
    return Response(status=HTTPStatus.OK)


@app.get("/users/<int:user_id>/posts")
def get_sorted_user_posts_by_reactions(user_id):
    data = request.get_json()
    try:
        sort_type = data["sort"]
    except KeyError:
        return Response(
            json.dumps({"error": "no found sort type"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if not models.check_sort_type(sort_type):
        return Response(
            json.dumps({"error": "unsupported sort type"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if not models.User.check_user_id(user_id):
        return Response(
            json.dumps({"error": "user with this id does not exist"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    user = USERS[user_id]
    posts = user.get_sorted_posts(sort_type)
    response = Response(
        models.JSONEncoder().encode(
            {"posts": [get_post(post.post_id).get_json() for post in posts]}
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_leaderboard():
    data = request.get_json()
    try:
        response_type = data["type"]
    except KeyError:
        return Response(
            json.dumps({"error": "response type not found"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if not models.check_response_type(response_type):
        return Response(
            json.dumps({"error": "unsupported response type"}),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    if response_type == "list":
        try:
            sort_type = data["sort"]
        except KeyError:
            return Response(
                json.dumps({"error": "no found sort type"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )

        if not models.check_sort_type(sort_type):
            return Response(
                json.dumps({"error": "unsupported sort type"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
        sorted_list = models.get_sorted_users(USERS, sort_type)
        response = Response(
            models.JSONEncoder().encode(
                {"users": [get_user(user.user_id).get_json() for user in sorted_list]}
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif response_type == "graph":
        sorted_users = models.get_sorted_users(USERS, "asc")
        fig, ax = plt.subplots()

        user_names = [
            f"{user.first_name} {user.last_name} ({user.user_id})"
            for user in sorted_users
        ]
        user_count_reactions = [user.total_reactions for user in sorted_users]

        ax.bar(user_names, user_count_reactions)

        ax.set_ylabel("User's reactions")
        ax.set_title("User leaderboard by quantity reactions")
        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    return Response(status=HTTPStatus.BAD_REQUEST)
