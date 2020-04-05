from app import app

import json

from flask import request, render_template, redirect

from app.extra import *



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
        return render_template('posts.html', data=data)


# @app.route('/echo', methods=['POST'])
# def echo():
#     # print(request.is_json)
#     if request.is_json:
#         content = request.get_json(force=True)
#     elif request.form:
#         content = request.form
#     else:
#         content = None

#     print(content)
#     return jsonify(content)


@app.route('/posts/<_id>/', methods=['GET', 'POST', 'DELETE'])
# @cache.cached()
def post(_id):
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
        return redirect(f'/posts/{_id}/')

    elif request.method == 'DELETE':

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

        data = set_post(content)
        return f'Post saved with "_id" = {data}'


@app.route('/api/posts/<_id>/', methods=['GET'])
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


@app.route('/api/statistics/<_id>/', methods=['GET'])
# @cache.cached()
def api_statistics(_id):

    data = get_post_statistics(_id)

    return json.dumps(data)
