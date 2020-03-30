from app import app

from flask import render_template
from flask import request

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/')
def posts():
    if request.method == 'GET':
        req = request.args.get('slug', '')
        return render_template('posts.html', slug=req)
    
    if request.method == 'POST':
        pass