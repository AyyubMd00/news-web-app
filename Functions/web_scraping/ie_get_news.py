from bs4 import BeautifulSoup
import requests


from web_scraping.ie_get_story import get_story
from utils.db_utils import upload_stories_in_db, is_story_present_in_db
# from utils.get_category_bert import get_category

def get_news():
    response = requests.get('https://indianexpress.com/section/cities/')
    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    nation_element = soup.find(class_='nation')

    stories = []
    news_count = 0
    for news_element in nation_element.find_all(class_='articles'):
        news_url = news_element.find(class_='img-context').find(class_='title').find('a').get('href')
        news_count += 1
        # print(news_count, news_url)

        if is_story_present_in_db(news_url)==True:
            continue
        story = get_story(news_url)
        # print("Story: ", story)
        if story != {}:
            # story['category'] = get_category(story['title'], story['description'])
            story['category'] = ''
            stories.append(story)
    if len(stories):
        upload_stories_in_db(stories)
# get_news()