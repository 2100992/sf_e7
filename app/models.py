from app.mongo_client import posts, comments, tags
from datetime import datetime
from slugify import slugify

class Post:
    _id = ''
    user_id = ''
    title = ''
    slug = ''
    text = ''
    short_text = ''
    created_date = None

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.title = data.get('title')
        self.text = data.get('text')
        if len(self.text) > 40:
            self.short_text = self.text[:37] + "..."
        else:
            self.short_text = self.text
        self.created_date = datetime.now()
        self.slug = slugify(self.title)

    def get_statistics(self):
        pass

    def find_one(self, id):
        result_post = posts.find_one({'_id':id})
        result_comments = comments.find({'post_id':id})
        result_tags = tags.find({'post_id':id})
        return result
    
    def get_all_posts(self):
        all_posts = posts.find()
        result = {}
        result['posts'] = []
        for post in all_posts:
            post_data = {}
            post_data['_id'] = self._id

            result['posts'].append(post_data)


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
        return self._id


class Comment:
    pass

class Tag:
    pass