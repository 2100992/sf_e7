import json

# from app.mongo_client import *
from app.models import Post
from app.redis_client import redis_client

from bson.objectid import ObjectId


def main():
    with open('./data4experiments/tst.json') as json_data:
        d = json.load(json_data)
        print(d)


def get_post_data():
    with open('./data4experiments/tst_post.json') as json_data:
        d = json.load(json_data)

    post = Post(d)
    _id = post.save()
    readed_post = Post({}).get_post(_id)
    print(readed_post)


def set_post_to_redis(post: dict) -> None:
    _id = post['_id']
    json_data = json.dumps(post)
    redis_client.set(f'post:id:{_id}', json_data)


def get_post_from_redis(_id) -> dict:
    result = json.loads(redis_client.get(f'post:id:{_id}'))
    return result


if __name__ == "__main__":
    # main()
    get_post_data()
