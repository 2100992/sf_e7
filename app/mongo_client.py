from pymongo import MongoClient
from app.config import MONGO_HOST, MONGO_PORT

mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)

# база данных callboard
callboard = mongo_client.callboard

# коллекция постов
posts = callboard.posts

# коллекция комментариев
comments = callboard.comments

# коллекция тегов
tags = callboard.tags



def main():

    posts_cursor = posts.find()
    print(f'\nposts_cursor\n{posts_cursor}')

    comments_cursor = comments.find()
    print(f'\ncomments_cursor\n{comments_cursor}')

    tags_cursor = tags.find()
    print(f'\ntags_cursor\n{tags_cursor}')


if __name__ == "__main__":
    main()
