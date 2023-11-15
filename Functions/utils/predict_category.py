import requests
from urllib import parse

from utils.db_utils import get_undefined_category_items, update_category_in_db

def predict_category():
    items = get_undefined_category_items()
    for item in items:
        url = 'https://api.freegpt4.ddns.net/?text='
        prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
        Out of the above categories, determine the category below news' title and description belongs to.
        Title: {item['title']}
        Description: {item['description']}
        Response should contain only one word ie, <category>.
        Note: Anything that involves government bodies and similar news belongs to nation.'''
        encoded_prompt = parse.quote(prompt)
        # print(encoded_prompt)
        response = requests.get(url+encoded_prompt)
        category = response.content.decode()
        if category.find('*') != -1:
            category = category[category.find('*')+2:category.rfind('*')-1]
        # print(category)
        update_category_in_db(item, category)

predict_category()