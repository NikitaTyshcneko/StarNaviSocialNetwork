import os
import string
import random
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)


def string_generator(string_size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(string_size))


def set_full_url(additional: str):
    return os.getenv('BASEURL') + additional


def login(user_data: dict, cookies):
    tokens = requests.post(set_full_url('api/token/'), data=user_data, cookies=cookies)
    return {"Authorization": "Bearer " + tokens.json()['access']}


def signup_user(data: dict, cookies):
    return requests.post(set_full_url('register/'), data=data, cookies=cookies)


def create_post(new_post: dict, headers: dict, cookies):
    return requests.post(set_full_url('api/v1/post/'), data=new_post, headers=headers, cookies=cookies)


def get_posts(headers: dict, cookies):
    return requests.get(set_full_url('api/v1/post/'), headers=headers, cookies=cookies)


def random_post_from_list(posts: list):
    index = random.randint(1, len(posts))
    random_posts = random.sample(posts, index)
    return random_posts


def like_post(post_id: int, headers: dict, cookies):
    return requests.post(set_full_url(f'api/v1/post/{post_id}/like/'), headers=headers, cookies=cookies)
