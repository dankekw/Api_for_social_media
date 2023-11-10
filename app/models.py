import re, json
from app import USERS, POSTS


def get_sorted_users(users, sort_type):
    sorted_users = sorted(users, key=lambda user: user.total_reactions)
    if sort_type == "asc":
        return sorted_users
    else:
        return sorted_users[::-1]


def check_sort_type(sort_type):
    if sort_type not in ["asc", "desc"]:
        return False
    return True


def check_response_type(response_type):
    if response_type not in ["list", "graph"]:
        return False
    return True


class User:
    def __init__(self, user_id, first_name, last_name, email, total_reactions=0):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = []

    @staticmethod
    def check_email(email):
        if len(email) > 7:
            if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None:
                return True
        return False

    @staticmethod
    def check_user_id(user_id):
        if isinstance(user_id, int):
            if 0 <= user_id < len(USERS):
                return True
        return False

    def get_sorted_posts(self, sort_type):
        posts = sorted(self.posts, key=lambda post: post.get_count_reactions())
        if sort_type == "asc":
            return posts
        else:
            return posts[::-1]


class Post:
    def __init__(self, post_id, author_id, text):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    @staticmethod
    def check_post_text(text):
        if isinstance(text, str):
            return True
        else:
            return False

    @staticmethod
    def check_post_id(post_id):
        if 0 <= post_id < len(POSTS):
            return True
        else:
            return False

    def get_count_reactions(self):
        return len(self.reactions)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
