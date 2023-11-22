from utils.db_utils import get_undefined_category_items, update_category_in_db
from utils.palm_predict_category_prompt import predict_category_prompt

def predict_category():
    items = get_undefined_category_items()
    for item in items:
        category = predict_category_prompt(item['title'], item['description'])
        if category:
            update_category_in_db(item, category)

# predict_category()