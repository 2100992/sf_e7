import os

from distutils.util import strtobool

HOST = str(os.environ.get('HOST', '127.0.0.1'))
PORT = int(os.environ.get('PORT', '5000'))
DEBUG = strtobool(os.environ.get('DEBUG','True'))


MONGO_HOST = str(os.environ.get('HOST', '192.168.1.20'))
MONGO_PORT = int(os.environ.get('PORT', '27017'))


REDIS_HOST = str(os.environ.get('HOST', '192.168.1.20'))
REDIS_PORT = int(os.environ.get('PORT', '6379'))