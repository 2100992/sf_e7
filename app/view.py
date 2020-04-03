from app import app

import json

from flask import request, render_template

from app.config import mongo, cache

from bson.objectid import ObjectId

# EXTRA FUNCTIONS______________________________________________________________


def get_posts(data={}) -> dict:

    result = {'posts': []}
    for post in mongo.db.posts.find(data):
        post['_id'] = str(post['_id'])
        post.update(get_post_statistics(str(post['_id'])))
        post.update(get_tags(str(post['_id'])))
        result['posts'].append(post)

    return result


def get_tags(post_id: str) -> dict:
    result = {}

    result['tags'] = []
    for tag in mongo.db.tags.find({'post_id': post_id}):
        tag['_id'] = str(tag['_id'])
        result['tags'].append(tag)

    return result


def get_comments(post_id: str) -> dict:
    result = {}

    result['comments'] = []
    for comment in mongo.db.comments.find({'post_id': post_id}):
        comment['_id'] = str(comment['_id'])
        result['comments'].append(comment)

    return result


def get_post(post_id: str) -> dict:
    result = {}

    if len(post_id) != 24:
        post_id = ''

    result['post'] = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
    result['post']['_id'] = str(result['post']['_id'])

    result.update(get_comments(post_id))
    result.update(get_tags(post_id))

    return result


def get_post_statistics(post_id: str) -> dict:
    result = {}

    comments = get_comments(post_id)
    tags = get_tags(post_id)

    result['statistics'] = {
        'comments': len(comments['comments']),
        'tags': len(tags['tags'])
    }

    return result


# END EXTRA FUNCTIONS__________________________________________________________


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/', methods=['GET'])
# @cache.cached()
def posts():
    req = dict(request.args)

    data = get_posts(req)

    return render_template('posts.html', data=data)


@app.route('/posts/<_id>/', methods=['GET'])
@cache.cached()
def post(_id):

    data = get_post(_id)

    return render_template('post.html', data=data)


@app.route('/api/posts/', methods=['GET'])
# @cache.cached()
def api_posts():
    req = dict(request.args)

    data = get_posts(req)

    return json.dumps(data)


@app.route('/api/posts/<_id>/', methods=['GET'])
@cache.cached()
def api_post(_id):

    data = get_post(_id)

    return json.dumps(data)


@app.route('/api/statistics/<_id>/', methods=['GET'])
@cache.cached()
def api_statistics(_id):

    data = get_post_statistics(_id)

    return json.dumps(data)
