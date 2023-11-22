import os
from pymongo import MongoClient
from get_category import get_category

mongodb_conn_string = os.environ.get("mongodb_conn_string")
client = MongoClient(mongodb_conn_string)
db = client['news_app']
collection = db['english_news']
stories_list = collection.find({"location": { "$exists": False } })
for story in stories_list:
    story['category'] = get_category(story['title'], story['description'])
    collection.update_one(story)
client.close()