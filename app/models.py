import re
from app import USERS, POSTS


class User:
    def __init__(
            self, user_id, first_name, last_name, email, total_reactions=0, posts=[]
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

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


class Post:
    def __init__(self, post_id, author_id, text, reactions=[]):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions

    @staticmethod
    def check_post_text(text):
        # todo добавить проверку на мат
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
