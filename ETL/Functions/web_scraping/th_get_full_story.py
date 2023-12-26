from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from uuid import uuid4
# import sys

# sys.path.append("utils")
from utils.utils import get_iso_datetime, get_country

def get_full_story(url):
    chrome_options = Options()
    # chrome_options.binary_location = 'selenium\chrome-win64\chrome.exe'
    chrome_options.add_argument('--disable-clound-management') # To Remove an error not related to selenium
    chrome_options.add_argument('--headless') # Headless Browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # print("Current Story Link:", driver.current_url)

    story = {
        "article_id": str(uuid4()),
        "source_id": "thehindu",
        "link": url,
        "language": "english",
        "video_url": "",
        "tags": []
        }

    article_element = driver.find_element(By.CLASS_NAME,'article-section')
    try:
        story['title'] = article_element.find_element(By.CLASS_NAME, 'title').text
    except:
        return {}
    try:
        story['description'] = article_element.find_element(By.CLASS_NAME, 'sub-title').text
    except:
        story['description'] = ''
    try:
        picture_element = article_element.find_element(By.CLASS_NAME, 'article-picture')
        picture_source_element = picture_element.find_element(By.TAG_NAME, 'source')
        story['image_url'] = picture_source_element.get_attribute('srcset')
    except:
        story['image_url'] = ""
    time_city_details = article_element.find_element(By.CLASS_NAME, 'publish-time').text
    published_time = time_city_details[:time_city_details.find('|')-1]
    updated_time = published_time[:-8] + time_city_details[time_city_details.rfind('Updated ')+8:time_city_details.find(' -')-3]
    # print(published_time, updated_time)
    story['published_timestamp'] = get_iso_datetime(published_time.strip(), "%B %d, %Y %I:%M %p")
    story['updated_timestamp'] = get_iso_datetime(updated_time.strip(), "%B %d, %Y %I:%M %p")
    city_name = ""
    if time_city_details.find('-')>-1:
        city_name = time_city_details[time_city_details.find('-')+2:]
    story['city_name'] = city_name
    # print(story['city_name'])
    if city_name.find(',')>-1: # If country also is included in the time city details
        story['city_name'] = city_name[city_name.find(','):]
    # print(story['city_name'])
    story['country'] = get_country(story['city_name'])
    try:
        story['author'] = article_element.find_element(By.CLASS_NAME, 'author').find_element(By.TAG_NAME, 'a').text
    except:
        story['author'] = ""
    try:
        content_element = article_element.find_element(By.CLASS_NAME, 'articlebodycontent')
    except:
        return {}
    story['content'] = []
    for para_element in content_element.find_elements(By.TAG_NAME, 'p'):
        para = para_element.text
        if 'COMMENTS' in para:
            break
        story['content'].append(para)

    return story

# print(get_full_story("https://www.thehindu.com/sport/races/kings-ransom-should-make-amends-in-the-parimatch-indian-st-leger/article67338090.ece"))