import json

from app.mongo_client import posts, comments, tags
from app.redis_client import redis_client
from datetime import datetime
from slugify import slugify

from bson.objectid import ObjectId


class Post:
    """

    """
    _id = ''
    data = {}

    def __init__(self, data={}) -> None:
        self.data = data

        if not self.data.get('user_id'):
            self.data['user_id'] = 'Anonymous'

        if self.data.get('text'):
            if len(self.data['text']) >= 40:
                self.data['short_text'] = self.data['text'][:37] + "..."
            else:
                self.data['short_text'] = self.data['text']

    def __str__(self) -> str:

        def return_level(data={}, s='',  l='') -> str:
            for key, value in data.items():
                s += f'\n{l} {key}'
                if isinstance(value, dict):
                    s += return_level(data[key], '', l + '-')
                elif (isinstance(value, list) or isinstance(value, set)):
                    for v in value:
                        return_level(v, s, l + '-')
                elif (isinstance(value, str) or isinstance(value, float) or isinstance(value, int)):
                    s += f' = {value}'
                else:
                    print('error')
                    s += '\nERROR'
                    return s
            return s

        result = return_level(self.data)
        return result

    def get_statistics(self, id) -> dict:
        """
        Получение статистики по id поста
        В статистике количество комментариев и тегов
        """
        result = {}

        redis_comments = redis_client.get(f'comments:id:{id}')
        _comments = redis_comments or [
            comment for comment in comments.find({'post_id': id})]

        if _comments:
            result['comments_count'] = len(_comments)
        else:
            result['comments_count'] = 0

        redis_tags = redis_client.get(f'tags:id:{id}')
        _tags = redis_tags or [
            tag for tag in tags.find({'post_id': id})]

        if _tags:
            result['tags_count'] = len(_tags)
        else:
            result['tags_count'] = 0

        return result

    def get_post(self) -> None:
        """
        Забираем пост по его id
        """
        _id = self.data['_id']
        result = {}

        redis_post = redis_client.get(f'post:id:{_id}')

        if redis_post:
            result = json.loads(redis_post)
            print('post from redis')
        else:
            result = posts.find_one({'_id': ObjectId(_id)})
            if result:
                result['_id'] = str(result['_id'])
                print('post from mongo')
                redis_client.set(
                    f'post:id:{result["_id"]}', json.dumps(result))
            else:
                print('No post')

        self.data = result

    def get_full_data_post(self) -> dict:
        """
        Забираем пост по его id вместе с соответствующими комментариями и тегами
        """

        redis_full_data_post = redis_client.get(
            f'full_data_post:id:{self.data["_id"]}')

        result = {}
        if redis_full_data_post:
            result = json.loads(redis_full_data_post)
            print('full data from redis')
        else:
            result['_id'] = self.data['_id']

            self.get_post()
            result['post'] = self.data
            result['comments'] = get_comments(self.data['_id'])
            result['tags'] = get_tags(self.data['_id'])
            print('full data from mongo')
            redis_client.set(
                f'full_data_post:id:{result["_id"]}', json.dumps(result))

        return result

    def save(self) -> str:
        self.data['created_date'] = datetime.now().timestamp()

        result = posts.insert_one(self.data)

        self.data['_id'] = str(result.inserted_id)

        redis_client.set(f'post:id:{self.data["_id"]}', json.dumps(self.data))
        redis_client.delete(f'post:all')

        return self.data['_id']


class Comment:
    def __init__(self, data={}) -> None:
        self.data = data

        if not self.data.get('user_id'):
            self.data['user_id'] = 'Anonymous'

        if self.data.get('text'):
            if len(self.data['text']) >= 40:
                self.data['short_text'] = self.data['text'][:37] + "..."
            else:
                self.data['short_text'] = self.data['text']

    def __str__(self) -> str:

        def return_level(data={}, s='',  l='') -> str:
            for key, value in data.items():
                s += f'\n{l} {key}'
                if isinstance(value, dict):
                    s += return_level(data[key], '', l + '-')
                elif (isinstance(value, list) or isinstance(value, set)):
                    for v in value:
                        return_level(v, s, l + '-')
                elif (isinstance(value, str) or isinstance(value, float) or isinstance(value, int)):
                    s += f' = {value}'
                else:
                    print('error')
                    s += '\nERROR'
                    return s
            return s

        result = return_level(self.data)
        return result

    def save(self) -> str:
        self.data['created_date'] = datetime.now().timestamp()

        result = comments.insert_one(self.data)

        self.data['_id'] = str(result.inserted_id)

        redis_client.set(f'comment:id:{self.data["_id"]}', json.dumps(self.data))
        redis_client.delete(f'comment:all')
        redis_client.delete(f'full_data_post:id:{self.data["_id"]}')

        return self.data['_id']


class Tag:
    pass


def get_all_posts() -> dict:
    """
    Получение списка всех постов в базе
    """
    result = {}

    redis_posts = redis_client.get(f'post:all')

    if redis_posts:
        result = json.loads(redis_posts)
        print('all posts from redis')
    else:
        all_posts = posts.find()
        if all_posts:
            result = {'posts': []}
            for post in all_posts:
                post['_id'] = str(post['_id'])
                result['posts'].append(post)

            print('all posts from mongo')

            redis_client.set(f'post:all', json.dumps(result))

    return result


def del_post(_id) -> None:
    posts.delete_one({'_id': ObjectId(_id)})
    redis_client.delete(f'post:id:{_id}')
    redis_client.delete(f'post:all')
    redis_client.delete(f'full_data_post:id:{_id}')


def get_comments(post_id: str) -> list:
    result = [c for c in comments.find({'post_id': post_id})]
    return result


def get_tags(post_id: str) -> dict:
    result = {}
    return result
