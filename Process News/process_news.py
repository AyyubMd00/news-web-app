from pymongo import MongoClient
from get_category import get_category

client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
db = client['news_app']
collection = db['english_news']
stories_list = collection.find({"location": { "$exists": False } })
for story in stories_list:
    story['category'] = get_category(story['title'], story['description'])
    collection.update_one(story)
client.close()