from app import app, USERS, models
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
        return Response("{'error': 'not valid email'}", status=201, mimetype='application/json')
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
    response = Response(
        json.dumps({
            "id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response
