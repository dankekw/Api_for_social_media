import re


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
