
import logging

from flask import Flask, render_template, jsonify, request, redirect

from utils import get_posts_all, get_comments_by_post_id, get_post_by_pk, get_posts_by_user, search_for_posts, \
    posts_found_by_tag, read_bookmarks_file, write_to_the_file_bookmarks

logger_first = logging.getLogger("first")

file_handler = logging.FileHandler('logs/api.log')  # логирование
formatter_first = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s ')
file_handler.setFormatter(formatter_first)
file_handler.setLevel(logging.INFO)
logger_first.addHandler(file_handler)
stream_logging_handler = logging.StreamHandler()
stream_logging_handler.setFormatter(formatter_first)
stream_logging_handler.setLevel(logging.DEBUG)
logger_first.addHandler(stream_logging_handler)
logger_first.setLevel(logging.DEBUG)
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/')
def all_posts():
    """Функция отображения всех постов"""
    content = get_posts_all()
    count_bookmarks = len(read_bookmarks_file())
    return render_template("index.html", content=content, count_bookmarks=count_bookmarks)


@app.route('/posts/<post_id>')
def get_comments(post_id):
    """Функция отображения постов по id"""
    post_match = get_post_by_pk(post_id)
    matched_comments = get_comments_by_post_id(post_id)
    return render_template("post.html", post_match=post_match, matched_comments=matched_comments)


@app.route('/search/')
def search_page():
    """Функция поиска постов"""
    s = request.args['s']
    posts_found = search_for_posts(s)
    return render_template("search.html", posts_found=posts_found)


@app.route('/users/<user_name>')
def get_posts_by_username(user_name):
    """Функция отображения всех пользователей"""
    matched_posts = get_posts_by_user(user_name)
    return render_template("user-feed.html", matched_posts=matched_posts)


@app.route('/tag/<tag_name>/')
def search_by_tag(tag_name):
    """Функция отображения постов по тэгу"""
    matched_posts = posts_found_by_tag(tag_name)
    return render_template("tag.html", matched_posts=matched_posts, tag_name=tag_name)


@app.route('/api/posts/')
def get_all_posts():
    """Функция отображения списка постов в JSON"""
    posts = get_posts_all()
    logger_first.info('запрошен /api/posts/')
    return jsonify(posts)


@app.route('/api/posts/<post_id>')
def get_post_by_id(post_id):
    """Функция отображения поста в JSON"""
    post_by_id = get_post_by_pk(post_id)
    logger_first.info(f"запрошен /api/posts/{post_id}")
    logger_first.debug(f"результат {post_by_id}")
    return jsonify(post_by_id)


@app.route('/bookmarks/add/<post_id>', methods=['POST'])
def save_post_in_bookmarks(post_id):
    """Функция отображения сохраненных закладок"""
    save_post = get_post_by_pk(post_id)
    bookmarks_content = read_bookmarks_file()
    bookmarks_content.append(save_post)
    write_to_the_file_bookmarks(bookmarks_content)
    return redirect("/", code=302)


@app.route('/bookmarks/remove/<post_id>', methods=['POST'])
def remove_post_from_bookmarks(post_id):
    """Функция удаления вкладки по id поста"""
    bookmarks_content_r = read_bookmarks_file()
    for post in bookmarks_content_r:
        if post['pk'] == int(post_id):
            index = bookmarks_content_r.index(post)
            bookmarks_content_r.pop(index)
    write_to_the_file_bookmarks(bookmarks_content_r)
    return redirect("/", code=302)


@app.route("/bookmarks")
def view_all_bookmarks():
    """Функция отображения всех закладок"""
    saved_bookmarks = read_bookmarks_file()
    return render_template("bookmarks.html", saved_bookmarks=saved_bookmarks)



@app.errorhandler(404)
def not_found_page(error):
    return "404 error"


@app.errorhandler(500)
def not_found_page(error):
    return "500 error"


if __name__ == "__main__":
    app.run()
