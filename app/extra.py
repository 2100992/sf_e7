from app import app

from datetime import datetime

from app.config import mongo

from bson.objectid import ObjectId

from slugify import slugify


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

        if not comment.get('created_date'):
            comment['created_date'] = 0

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


def set_post(data={}) -> str:
    result = ''

    if not data.get('user_id'):
        data['user_id'] = 'Anonymous'

    if data.get('text'):
        if len(data['text']) >= 40:
            data['short_text'] = data['text'][:37] + "..."
        else:
            data['short_text'] = data['text']

    if data.get('title'):
        if len(data['title']) >= 40:
            data['title'] = data['title'][:37] + "..."
        data['slug'] = slugify(data['title'])

    data['created_date'] = datetime.now().timestamp()

    result = mongo.db.posts.insert_one(data)

    post_id = str(result.inserted_id)

    tags = data.get('tags')
    tags_set = set(tags.split())

    if tags:
        for t in tags_set:
            tag_data = {
                'tag': t,
                'user_id': data['user_id'],
                'post_id': post_id
            }
            set_tag(tag_data)

    return post_id


def set_tag(data={}) -> str:
    if not data.get('user_id'):
        data['user_id'] = 'Anonymous'

    data['created_date'] = datetime.now().timestamp()

    mongo.db.tags.insert_one(data)

    return f'Saved tag for post - {data["post_id"]}'


def set_comment(data={}) -> str:

    if not data.get('user_id'):
        data['user_id'] = 'Anonymous'

    data['created_date'] = datetime.now().timestamp()

    mongo.db.comments.insert_one(data)

    return f'Saved comment for post - {data["post_id"]}'


def delete_post(post_id: str) -> str:
    if len(post_id) != 24:
        post_id = ''

    deleted_post = mongo.db.posts.delete_one({'_id': ObjectId(post_id)})

    result = f'deleted {deleted_post.deleted_count} post'
    result += delete_comments(post_id)
    result += delete_tags(post_id)
    return result


def delete_tags(post_id: str) -> str:

    result = mongo.db.tags.delete_many({'post_id': post_id})

    return f'\ndeleted {result.deleted_count} tags'


def delete_comments(post_id: str) -> str:

    result = mongo.db.comments.delete_many({'post_id': post_id})

    return f'\ndeleted {result.deleted_count} comments'

# END EXTRA FUNCTIONS__________________________________________________________


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):

    if date == 0:
        return ''
    else:
        date = datetime.fromtimestamp(date) 
        native = date.replace(tzinfo=None)
        format='%b %d, %Y'
        return native.strftime(format)