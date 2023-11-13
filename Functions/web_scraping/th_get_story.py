from bs4 import BeautifulSoup
import requests
from uuid import uuid4
from datetime import datetime

from utils.utils import get_iso_datetime, get_country

def get_story(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    story = {
        "article_id": str(uuid4()),
        "source_id": "thehindu",
        "link": url,
        "language": "english",
        "video_url": "",
        "tags": [],
        "created_timestamp": (datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    article_element = soup.find(class_='article-section')
    title_element = article_element.find(class_= 'title')
    if title_element == None:
        return {}
    story['title'] = title_element.get_text().strip()
    description_element = article_element.find(class_= 'sub-title')
    if description_element != None:
        story['description'] = description_element.get_text().strip()
    else:
        story['description'] = ''
    picture_element = article_element.find(class_= 'article-picture')
    try:
        picture_source_element = picture_element.find('source') # if picture_element is None, it will throw error here.
        story['image_url'] = picture_source_element.get('srcset') # if picture_source_element is None, it will throw error here.
    except:
        story['image_url'] = ""
    time_city_details = article_element.find(class_= 'publish-time').get_text().strip()
    published_time = time_city_details[:time_city_details.find('|')-1]
    # updated_time = published_time[:-8] + time_city_details[time_city_details.rfind('Updated ')+8:time_city_details.find(' -')-3]
    # print(published_time, updated_time)
    story['published_timestamp'] = get_iso_datetime(published_time.strip(), "%B %d, %Y %I:%M %p")
    # story['updated_timestamp'] = get_iso_datetime(updated_time.strip(), "%B %d, %Y %I:%M %p")
    city_name = ""
    if time_city_details.find('-')>-1:
        city_name = time_city_details[time_city_details.find('-')+2:]
    story['city_name'] = city_name
    # print(story['city_name'])
    if city_name.find(',')>-1: # If country also is included in the time city details
        story['city_name'] = city_name[city_name.find(','):]
    # print(story['city_name'])
    story['country'] = get_country(story['city_name'])
    author_element = article_element.find(class_= 'author').find('a')
    if author_element != None:
        story['author'] = author_element.get_text().strip()
    else:
        story['author'] = ""
    content_element = article_element.find(class_= 'articlebodycontent')
    if content_element == None:
        return {}
    story['content'] = []
    for para_element in content_element.find_all('p'):
        para = para_element.get_text().strip()
        if 'comments' in para.lower():
            break
        story['content'].append(para)

    return story
