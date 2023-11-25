from bs4 import BeautifulSoup
import requests

from web_scraping.th_get_story import get_story
from utils.db_utils import upload_stories_in_db, is_story_present_in_db
from utils.utils import is_english_news
# from utils.get_category_bert import get_category

def get_news():
    response = requests.get('https://www.thehindu.com/latest-news/')
    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    news_element = soup.find(class_='latest-news')

    news_count = 0
    stories = []
    for news_element in news_element.find_all('li'):
        news_count += 1
        category = news_element.find_all('a')[1].text
        if category not in ['PREMIUM', 'SPONSORED CONTENT', 'NEWS']:
            link_element = news_element.find('a')
            link = link_element.get('href')
            title = link_element.get_text().strip()
            if is_english_news(title) == False:
                continue
            if link_element.find(class_='picture') == None:
                return
            print(news_count, link)
            if is_story_present_in_db(link)==True:
                continue
            story = get_story(link, title)
            # print(story)
            if story != {}:
                # story['category'] = get_category(story['title'], story['description'])
                story['category'] = ''
                stories.append(story)
    if len(stories):
        upload_stories_in_db(stories)