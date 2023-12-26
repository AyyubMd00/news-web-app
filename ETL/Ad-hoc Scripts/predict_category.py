import sys

sys.path.append('Functions\\utils')
from palm_predict_category_prompt import predict_category_prompt
from db_utils import query_stories, update_category_in_db

query = {'created_timestamp': {'$lt': '2023-11-24T00:00:00.00000Z'}}
items = list(query_stories(query))
print(len(items))
for item in items:
    print(item['title'], item['description'], sep='\n')
    category = predict_category_prompt(item['title'], item['description'])
    print(category)
    if category:
        update_category_in_db(item, category)