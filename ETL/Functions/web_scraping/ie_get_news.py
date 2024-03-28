from bs4 import BeautifulSoup
import requests

from web_scraping.ie_get_story import get_story
from utils.db_utils import upload_stories_in_db, is_story_present_in_db
from utils.utils import is_english_news
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
        title_element = news_element.find(class_='img-context').find(class_='title').find('a')
        news_url = title_element.get('href')
        news_title = title_element.get_text().strip()
        if is_english_news(news_title) == False:
            continue
        news_count += 1
        # print(news_count, news_url)

        if is_story_present_in_db(news_url)==True:
            continue
        story = get_story(news_url, news_title)
        # print("Story: ", story)
        if story != {}:
            # story['category'] = get_category(story['title'], story['description'])
            # story['category'] = ''
            stories.append(story)
    if len(stories):
        upload_stories_in_db(stories)
# get_news()