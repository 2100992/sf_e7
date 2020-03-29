from pymongo import MongoClient
mongo_client = MongoClient()

new_db = mongo_client.newdb

new_collection = new_db.new_collection

cursor = new_collection.find()

print(cursor)