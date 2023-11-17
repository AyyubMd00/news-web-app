import requests
from urllib import parse

def predict_category_prompt(title, description):
    url = 'https://api.freegpt4.ddns.net/?text='
    prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
    Out of the above categories, determine the category below news' title and description belongs to.
    Title: {title}
    Description: {description}
    Response should contain only one word ie, <category>.
    Note: Anything that involves government bodies and similar news belongs to nation.'''
    encoded_prompt = parse.quote(prompt)
    # print(encoded_prompt)
    response = requests.get(url+encoded_prompt)
    category = response.content.decode()
    if category.find('*') != -1:
        category = category[category.find('*')+2:category.rfind('*')-1]
    # print(category)
    return category