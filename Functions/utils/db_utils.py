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

def is_story_present_in_db(link):
    client = MongoClient('mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/')
    db = client['news_app']
    collection = db['english_news']
    query_result = collection.find({'link': link})
    if len(list(query_result)):
        return True
    return False