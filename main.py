import logging

from flask import Flask, render_template, jsonify, request

from utils import get_posts_all, get_comments_by_post_id, get_post_by_pk, get_posts_by_user, search_for_posts

logger_first = logging.getLogger("first")

file_handler = logging.FileHandler('logs/api.log')
formatter_first = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s ')
file_handler.setFormatter(formatter_first)
file_handler.setLevel(logging.INFO)
logger_first.addHandler(file_handler)
# logger_first.setLevel(logging.INFO)
stream_logging_handler = logging.StreamHandler()
stream_logging_handler.setFormatter(formatter_first)
stream_logging_handler.setLevel(logging.DEBUG)
logger_first.addHandler(stream_logging_handler)
logger_first.setLevel(logging.DEBUG)
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/')
def all_posts():
    content = get_posts_all()
    return render_template("index.html", content=content)


@app.route('/posts/<post_id>')
def get_comments(post_id):
    post_match = get_post_by_pk(post_id)
    matched_comments = get_comments_by_post_id(post_id)
    return render_template("post.html", post_match=post_match, matched_comments=matched_comments)


@app.route('/search/')
def search_page():
    s = request.args['s']
    posts_found = search_for_posts(s)
    return render_template("search.html", posts_found=posts_found)


@app.route('/users/<user_name>')
def get_posts_by_username(user_name):
    matched_posts = get_posts_by_user(user_name)
    return render_template("user-feed.html", matched_posts=matched_posts)


@app.route('/api/posts/')
def get_all_posts():
    posts = get_posts_all()
    logger_first.info('запрошен /api/posts/')
    return jsonify(posts)


@app.route('/api/posts/<post_id>')
def get_post_by_id(post_id):
    post_by_id = get_post_by_pk(post_id)
    logger_first.info(f"запрошен /api/posts/{post_id}")
    logger_first.debug(f"результат {post_by_id}")
    return jsonify(post_by_id)


@app.errorhandler(404)
def not_found_page(error):
    return "404 error"


@app.errorhandler(500)
def not_found_page(error):
    return "500 error"


if __name__ == "__main__":
    app.run()