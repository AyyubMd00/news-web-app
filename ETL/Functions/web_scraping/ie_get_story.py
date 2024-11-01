from bs4 import BeautifulSoup
import requests
from uuid import uuid4
from datetime import datetime, timedelta

from utils.utils import get_iso_datetime

def get_story(url, title):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # print("Current Story Link:", url)

    story = {
        "article_id": str(uuid4()),
        "source_id": "indianexpress",
        "title": title,
        "link": url,
        "country": "India",
        "language": "english",
        "created_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), #using utcnow instead now is because the azure function apps is set to utc timezone.
        "category": "",
        "tags": {}
    }

    title_element = soup.find(class_='heading-part')
    if title_element == None:
        print('title element missing')
        return {}
    if title_element.find(class_='ie-premium') != None:
        print("Premium story")
        return {}
    if title_element.find(class_='livegif') != None: # Return empty dictionary if it's a live blog
        print("Live blog")
        return {}
    video_element = soup.find(class_='ytp-impression-link')
    if video_element != None:
        story['video_url'] = video_element.get('href')
    else:
        story['video_url'] = ''
    story['description'] = title_element.find('h2').get_text().strip()

    author_element = soup.find(class_='editor')
    if author_element.find('a') != None: # If author is missing
        story['author'] = author_element.find('a').get_text().strip()
    else:
        story['author'] = ''
    # updated_timestamp = author_element.find('span').get_text().strip()
    # if 'Updated: ' in updated_timestamp:
    #     story['updated_timestamp'] = get_iso_datetime(updated_timestamp[9:], "%B %d, %Y %H:%M IST") # To remove Updated: 
    # else:
    #     story['updated_timestamp'] = get_iso_datetime(updated_timestamp, "%B %d, %Y %H:%M IST")
    if author_element.find('br') != None: # Search for the city
        story['city_name'] = author_element.find('br').get_text().strip()
    else:
        story['city_name'] = ''


    content_element = soup.find(class_='full-details')
    caption_element = content_element.find(class_='custom-caption')
    image_element = caption_element.find('img')
    if image_element != None: # If image is missing
        story['image_url'] = image_element.get('src')
    else:
        story['image_url'] = ''
    para_elements = content_element.find_all('p')
    if para_elements != None: # If content is missing, don't carry on with this story
        story['content'] = []
        count = 1
        for para_element in para_elements:
            story['content'].append(para_element.get_text().strip())
            # print(para_element.text, count)
            count += 1
        # story['content'] = story['content'][:-2] #This line was used when content was of type string to remove last '\n'.
        if 'Click here' in story['content'][-1]:
            story['content'] = story['content'][:-1]
    else:
        print("Content Missing")
        return {}
    first_publish_element = soup.find(class_='ie-first-publish')
    published_time_element = first_publish_element.find('span')
    if published_time_element != None: # If Published Timestamp is missing
        published_time = published_time_element.get_text().strip()
        print("Published Time:", published_time)
        story['published_timestamp'] = get_iso_datetime(published_time, "%B %d, %Y %H:%M IST")
    else:
        print("Published Timestamp Missing")
        return {}
    # tags_element = soup.find(class_='storytags')
    # if tags_element != None: # If tag is missing
    #     story['tags'] = []
    #     for tag_element in tags_element.find('li'):
    #         if 'tags' in tag_element.text.lower():
    #             continue
    #         story['tags'].append(tag_element.get_text().strip())
    # else:
    #     story['tags'] = {}
    return story