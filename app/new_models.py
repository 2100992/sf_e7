import json

from pymongo import MongoClient
from app.config import MONGO_HOST, MONGO_PORT
from bson.objectid import ObjectId

import redis
from app.config import REDIS_HOST, REDIS_PORT

mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)

# база данных callboard
callboard = mongo_client.callboard

# коллекция постов
mongo_posts = callboard.posts

# коллекция комментариев
mongo_comments = callboard.comments

# коллекция тегов
mongo_tags = callboard.tags

# коннект к redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


class Data:
    def __init__(self, data_type='', data={}) -> None:
        self.data = data
        self.data_type = data_type

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

        result = self.data_type + return_level(self.data)
        return result

    def get_data(self) -> None:
        result = {}
        if self.data_type == 'post':

            _id = self.data['_id']

            redis_post = redis_client.get(f'post:id:{_id}')

            if redis_post:
                result = json.loads(redis_post)
                print('post from redis')
            else:
                result = mongo_posts.find_one({'_id': ObjectId(_id)})
                if result:
                    result['_id'] = str(result['_id'])
                    print('post from mongo')
                    redis_client.set(
                        f'post:id:{result["_id"]}', json.dumps(result))
                else:
                    print('No post')
        elif self.data_type == 'comment':
            post_id = self.data['post_id']

            redis_comments = redis_client.get(f'comments:post_id:{post_id}')

            if redis_comments:
                result = json.loads(redis_comments)
                print('commentsfrom redis')
            else:
                result = [c for c in mongo_comments.find({'post_id': post_id})]
                # result = posts.find_one({'_id': ObjectId(_id)})
                if result:
                    result['_id'] = str(result['_id'])
                    print('post from mongo')
                    redis_client.set(
                        f'post:id:{result["_id"]}', json.dumps(result))
                else:
                    print('No post')

        self.data = result

    def save(self) -> str:
        result = ''
        return result
