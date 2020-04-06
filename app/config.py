import os

from app import app

from flask_caching import Cache
from flask_pymongo import PyMongo

from distutils.util import strtobool

HOST = str(os.environ.get('HOST', '127.0.0.1'))
PORT = int(os.environ.get('PORT', '5000'))
DEBUG = strtobool(os.environ.get('DEBUG', 'True'))


MONGO_HOST = str(os.environ.get('MONGO_HOST', '192.168.1.20'))
MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))


REDIS_HOST = str(os.environ.get('REDIS_HOST', '192.168.1.151'))
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))

DATA_BASE = 'callboard'

app.config["MONGO_URI"] = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATA_BASE}"
# app.config['MONGO_DBNAME'] = 'dashboard'
mongo = PyMongo(app)
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:6379/0',
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_IGNORE_ERRORS": True,
})
