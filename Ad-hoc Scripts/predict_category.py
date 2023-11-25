import sys

sys.path.append('Functions\\utils')
from palm_predict_category_prompt import predict_category_prompt
from db_utils import get_undefined_category_items, update_category_in_db

items = list(get_undefined_category_items(100000))
print(len(items))
for item in items:
    category = predict_category_prompt(item['title'], item['description'])
    if category:
        update_category_in_db(item, category)

