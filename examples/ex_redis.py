import redis
import csv


def get_data(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            yield row


def insert_sorted_set_value(redis_client, sorted_set_name, key, value):
    redis_client.zadd(sorted_set_name, {key: value})


def main():
    redis_client = redis.Redis(host='192.168.1.151', port=6379)
    data = get_data('csv_to_redis/data2.csv')
    for row in data:
        set_name, param, rank = row
        rank = float(rank)
        insert_sorted_set_value(redis_client, set_name, param, rank)


if __name__ == "__main__":
    main()
