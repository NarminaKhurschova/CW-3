import json


def get_posts_all():
    with open("data/posts.json") as file:
        all_posts = json.load(file)
        return all_posts


def get_posts_by_user(user_name):
    all_posts = get_posts_all()
    user_posts = []
    for user_post in all_posts:
        if user_post["poster_name"] == user_name:
            user_posts.append(user_post)
    if len(user_posts) == 0:
        raise ValueError
    else:
        return user_posts


def get_comments():
    with open("data/comments.json") as file:
        all_comments = json.load(file)
        return all_comments


def get_comments_by_post_id(post_id):
    all_comments = get_comments()
    comments_match = []
    post = int(post_id)
    for comment in all_comments:
        if comment["post_id"] == post:
            comments_match.append(comment)

    if len(comments_match) == 0:
        raise ValueError
    else:
        return comments_match


def search_for_posts(query):
    all_posts = get_posts_all()
    found_posts =[]
    for post in all_posts:
        text = post["content"].lower()
        if query in text:
            found_posts.append(post)
    return found_posts

def get_post_by_pk(pk):
    all_posts = get_posts_all()
    posts_pk = int(pk)
    for post in all_posts:
        if post['pk'] == posts_pk:
            return post





