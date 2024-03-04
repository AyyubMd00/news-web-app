from pymongo import MongoClient
import os

mongodb_conn_string = os.environ.get("mongodb_conn_string")
def upload_story_in_db(story):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    query_result = collection.find({'title': story['title']})
    if len(list(query_result)):
        return
    collection.insert_one(story)
    client.close()

def upload_stories_in_db(stories):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    collection.insert_many(stories)
    client.close()

def get_undefined_category_or_tag_items(limit):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    query = {
            'or': [
                {'category': ''},
                {'tags': {}}
            ]
        }
    project = {
        '_id': 1,
        'title': 1,
        'description': 1,
        'content': 1
    }
    items = collection.find(query, project).sort('created_timestamp', -1).limit(limit)
    return items

# def get_wrong_category_items(limit):
#     client = MongoClient(mongodb_conn_string)
#     db = client['news_app']
#     collection = db['english_news']
#     query = {'created_timestamp': {'$lt': '2023-11-23T00:00:00.000Z'}}
#     items = collection.find(query).sort('created_timestamp', -1).limit(limit)
#     return items

# def get_count_of_undefined_category():
#     client = MongoClient(mongodb_conn_string)
#     db = client['news_app']
#     collection = db['english_news']``
#     query = {'category': ''}
#     count = collection.count_documents(query)
#     return count


def update_category_and_tags_in_db(item, category, tags):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    update = {"$set": {"category": category, "category_predicted": True, "tags": tags, "tags_predicted": True}}
    collection.update_one({"_id": item["_id"]}, update)

def is_story_present_in_db(link):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    query_result = collection.find({'link': link})
    if len(list(query_result)):
        return True
    return False

def delete_stories(query):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    collection.delete_many(query)

def query_stories(query={}, sort=None, limit=None):
    client = MongoClient(mongodb_conn_string)
    db = client['news_app']
    collection = db['english_news']
    items = collection.find(query)
    if sort:
        items = items.sort(sort)
    if limit:
        items = items.limit(limit)
    return items