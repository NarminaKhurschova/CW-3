from main import app
from utils import get_posts_all


def all_keys():
    posts = get_posts_all()
    post = posts[0]
    keys = post.keys()
    return keys


def test_is_txt_list():
    response = app.test_client().get('/api/posts/')
    assert response.status_code == 200
    assert type(response.json) is list
    post = response.json[0]
    post_keys_list = list(post.keys())
    list_all_keys = all_keys()
    a = set(post_keys_list)
    b = set(list_all_keys)
    assert a == b,'нет такого элемента'




def test_is_dict():
    response = app.test_client().get('/api/post/<post_id>')
    assert response.status_code == 200
    print(response.json)






