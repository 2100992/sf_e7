import csv
import redis
from app.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def insert_sorted_set_value(redis_client, sorted_set_name, key, value):
    redis_client.zadd(sorted_set_name, {key: value})


def main():
    pass


if __name__ == "__main__":
    main()
