from app import app

import json

from flask import request, render_template, redirect, url_for

from app.extra import *

from app.config import cache

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/', methods=['GET', 'POST'])
# @cache.cached()
def posts():

    if request.method == 'GET':
        req = dict(request.args)

        data = get_posts(req)

        print(data)

        return render_template('posts.html', data=data)

    elif request.method == 'POST':
        content = dict(request.form)
        post_id = set_post(content)
        print(content)
        print(post_id)

        data = get_posts()
        return redirect(url_for('posts'))


@app.route('/posts/<_id>/', methods=['GET', 'POST'])
# @cache.cached()
def post(_id):

    print(f'request.method = {request.method}')

    if request.method == 'GET':

        data = get_post(_id)

        print(data)

        return render_template('post.html', data=data)

    elif request.method == 'POST':
        print('comment POST')

        content = dict(request.form)

        content['post_id'] = _id

        result = set_comment(content)
        print(result)

        data = get_post(_id)

        # return render_template('post.html', data=data)
        # return redirect(url_for('post'), _id)
        return redirect(f".")


@app.route('/post-delete/<_id>/', methods=['GET'])
def del_post(_id):
    if request.method == 'GET':

        deleted = delete_post(_id)

        print(deleted)

        return redirect('/posts/')


@app.route('/api/posts/', methods=['GET', 'POST'])
# @cache.cached()
def api_posts():
    if request.method == 'GET':
        req = dict(request.args)

        data = get_posts(req)

        return json.dumps(data)

    elif request.method == 'POST':
        content = request.get_json(force=True)

        result = set_post(content)
        return f'Post saved with "_id" = {result}'


@app.route('/api/posts/<_id>/', methods=['GET', 'POST'])
# @cache.cached()
def api_post(_id):
    if request.method == 'GET':

        data = get_post(_id)

        return json.dumps(data)

    elif request.method == 'POST':

        content = request.get_json(force=True)
        content['post_id'] = _id

        result = set_comment(content)
        return result

@app.route('/api/tag/<_id>/', methods=['POST'])
def api_tag(_id):
    if request.method == 'POST':
        content = request.get_json(force=True)
        content['post_id'] = _id
        result = set_tag(content)
        return result


@app.route('/api/statistics/<_id>/', methods=['GET'])
# @cache.cached()
def api_statistics(_id):

    data = get_post_statistics(_id)

    return json.dumps(data)
