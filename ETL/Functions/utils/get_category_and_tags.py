# from pprint import pprint

from utils.db_utils import get_undefined_category_or_tag_items, update_category_and_tags_in_db
from utils.gemini_ai_predict_category_prompt import predict_category_prompt
from utils.gemini_ai_get_tags import get_tags

def get_category_and_tags():
    items = get_undefined_category_or_tag_items(75)
    # print('Items:', items)
    item_count = 0
    for item in items:
        item_count += 1
        # print(item['title'], item['description'], sep='\n')
        category = predict_category_prompt(item['title'], item['description'])
        tags = get_tags(item['title'], item['description'], item['content'])
        if not tags:
            tags = {}
        # print(item_count, '. ', category, sep='')
        if category:
            update_category_and_tags_in_db(item, category, tags)

# predict_category()