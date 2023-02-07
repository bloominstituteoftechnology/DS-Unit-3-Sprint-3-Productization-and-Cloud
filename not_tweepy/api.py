from not_tweepy.user import User


class API:

    def __init__(self, *args, **kwargs):
        pass

    def get_user(self, screen_name: str):
        return User({"screen_name": screen_name})
