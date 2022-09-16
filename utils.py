import json


def get_posts_all():
    """Функция выгрузки всех постов из JSON файла"""
    with open("data/posts.json") as file:
        all_posts = json.load(file)
        return all_posts


def get_posts_by_user(user_name):
    """Функция поиска постов по имени пользователя"""
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
    """Функция выгрузки всех комментариев"""
    with open("data/comments.json") as file:
        all_comments = json.load(file)
        return all_comments


def get_comments_by_post_id(post_pk):
    """Функция поиска комментариев по id поста"""
    all_comments = get_comments()
    comments_match = []
    if get_post_by_pk(post_pk) is None:
        raise ValueError
    for comment in all_comments:
        if comment['post_id'] == int(post_pk):
            comments_match.append(comment)
    return comments_match


def search_for_posts(query):
    """Функция поиска постов по ключевому слову"""
    all_posts = get_posts_all()
    found_posts =[]
    for post in all_posts:
        text = post["content"].lower()
        if query in text:
            found_posts.append(post)
    return found_posts

def get_post_by_pk(pk):
    """Функция поиска постов по id"""
    all_posts = get_posts_all()
    posts_pk = int(pk)
    for post in all_posts:
        if post['pk'] == posts_pk:
            return post


def posts_found_by_tag(tag_name):
    """Функция поиска постов по тэгу"""
    posts = get_posts_all()
    matched_posts = []
    tag_with_name = "#" + tag_name
    for post in posts:
        if tag_with_name in post["content"]:
            matched_posts.append(post)
    return matched_posts


def read_bookmarks_file():
    """Функция выгрузки всех закладок"""
    with open('data/bookmarks.json', 'r') as file_r:
        content_file = json.load(file_r)
    return content_file


def write_to_the_file_bookmarks(content):
    """Функция перезаписи данных в файл"""
    with open("data/bookmarks.json", 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)
    return None







