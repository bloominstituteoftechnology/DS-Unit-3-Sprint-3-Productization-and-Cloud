from os import getenv
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()
URL = getenv("NOT_TWITTER_URL")


class Tweet:

    def __init__(self, data: Dict):
        self.full_text = ""
        self.__dict__.update(data)

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.full_text


class User:

    def __init__(self, data: Dict):
        self.screen_name = data.get('screen_name')
        user_data = requests.get(f"{URL}/user/{self.screen_name}").json()
        self.__dict__.update(user_data)

    def timeline(self, *args, **kwargs):
        return [
            Tweet(tweet)
            for tweet in requests.get(f"{URL}/read/{self.screen_name}").json()
        ]

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.screen_name
