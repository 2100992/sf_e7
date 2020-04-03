from app import app

from flask import render_template
from flask import request

from app.models import Post, get_all_posts


@app.route('/')
def index():

    # print(posts)
    return render_template('index.html')


@app.route('/posts/')
def posts():
    if request.method == 'GET':
        req = request.args.get('_id')
        if req:
            post = Post({'_id': req})
            data = post.get_full_data_post()
            return render_template('post.html', data=data)
        else:
            posts = get_all_posts()
            return render_template('posts.html', posts=posts['posts'])

    elif request.method == 'POST':
        pass
