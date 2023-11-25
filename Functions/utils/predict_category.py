from pprint import pprint

from utils.db_utils import get_undefined_category_items, update_category_in_db
from utils.palm_predict_category_prompt import predict_category_prompt

def predict_category():
    items = get_undefined_category_items(40)
    # print('Items:', items)
    item_count = 0
    for item in items:
        item_count += 1
        # print(item['title'], item['description'], sep='\n')
        category = predict_category_prompt(item['title'], item['description'])
        # print(item_count, '. ', category, sep='')
        if category:
            update_category_in_db(item, category)

# predict_category()