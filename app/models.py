from app.mongo_client import posts, comments, tags
from app.redis_client import redis_client
from datetime import datetime
from slugify import slugify


class Post:
    """
    
    """
    _id = ''
    user_id = ''
    title = ''
    slug = ''
    text = ''
    short_text = ''
    created_date = None

    def __init__(self, data) -> None:
        self.user_id = data.get('user_id')
        self.title = data.get('title')
        self.text = data.get('text')
        if len(self.text) > 40:
            self.short_text = self.text[:37] + "..."
        else:
            self.short_text = self.text
        self.created_date = datetime.now()
        self.slug = slugify(self.title)

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

    def get_post(self, id) -> dict:
        """
        Забираем пост по его id вместе с соответствующими комментариями и тегами
        """

        result = {}
        result['id'] = id

        redis_post = redis_client.get(f'post:id:{id}')
        result['post'] = redis_post or posts.find_one({'_id': id})

        redis_comments = redis_client.get(f'comments:id:{id}')
        result['comments'] = redis_comments or [
            comment for comment in comments.find({'post_id': id})]

        redis_tags = redis_client.get(f'tags:id:{id}')
        result['tags'] = redis_tags or [
            tag for tag in tags.find({'post_id': id})]

        return result

    def get_all_posts(self) -> dict:
        """
        Получение списка всех постов в базе
        """
        result = {}
        result['posts'] = [post for post in posts.find()]
        return result

    def save(self):
        data = {}
        data['user_id'] = self.user_id
        data['title'] = self.title
        data['slug'] = self.slug
        data['text'] = self.text
        data['short_text'] = self.short_text
        data['created_date'] = self.created_date

        result = posts.insert_one(data)
        self._id = result.inserted_id

        redis_client.set(f'post:id:{self._id}')

        return self._id


class Comment:
    pass


class Tag:
    pass
