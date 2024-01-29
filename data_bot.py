import requests
from bot.config import Config
from bot.utils import (set_full_url, string_generator, signup_user, login,
                       create_post, get_posts, random_post_from_list, like_post)

get_token = requests.get(set_full_url('register'))
list_of_new_users = []

for user in range(Config.number_of_users):
    password = string_generator()
    new_user = {
        'csrfmiddlewaretoken': get_token.cookies.get('csrftoken'),
        'username': string_generator(),
        'password': password,
        'confirm_password': password,
    }
    response = signup_user(new_user, get_token.cookies)
    list_of_new_users.append(new_user)

for user in list_of_new_users:
    user_data = {"username": user['username'], "password": user['password']}
    headers = login(user_data, get_token.cookies)

    for post in range(Config.max_posts_per_user):
        new_post = {
            "title": string_generator(10),
            "body": string_generator(50)
        }
        create_post(new_post, headers, get_token.cookies)

for user in list_of_new_users:
    login_data = {"username": user['username'], "password": user['password']}
    headers = login(login_data, get_token.cookies)
    posts = get_posts(headers, get_token.cookies)
    random_posts = random_post_from_list(posts.json()['results'])

    for post in random_posts:
        like_post(post["id"], headers, get_token.cookies)
