from pymongo import MongoClient

def upload_story_in_db(story):
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    query_result = collection.find({'title': story['title']})
    if len(list(query_result)):
        return
    collection.insert_one(story)
    client.close()

def upload_stories_in_db(stories):
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    collection.insert_many(stories)
    client.close()

def get_undefined_category_items():
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    query = {'category': ''}
    items = collection.find(query)
    return items

def update_category_in_db(item, category):
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    update = {"$set": {"category": category, "category_predicted": True}}
    collection.update_one({"_id": item["_id"]}, update)

def is_story_present_in_db(link):
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    query_result = collection.find({'link': link})
    if len(list(query_result)):
        return True
    return False