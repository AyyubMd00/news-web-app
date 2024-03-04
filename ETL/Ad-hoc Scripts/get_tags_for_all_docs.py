from gemini_ai_get_tags import get_tags
from db_utils import query_stories, update_category_and_tags_in_db

query = {
    'created_timestamp': {'$gt': '2024-01-01T00:00:00.00000Z'},
    '$or': [
        {'tags': []},
        {'tags': {}}
        ]
    }
items = list(query_stories(query))
print(len(items))
i=0
for item in items:
    i+=1
    print(i)
    tags = get_tags(item['title'], item['description'], item['content'])
    if not tags:
        tags = {}
    update_category_and_tags_in_db(item, item['category'], tags)