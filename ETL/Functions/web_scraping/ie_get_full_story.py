from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from uuid import uuid4
# import sys

# sys.path.append("utils")
from utils.utils import get_iso_datetime

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
        "source_id": "indianexpress",
        "link": url,
        "country": "India",
        "language": "english"
        }

    title_element = driver.find_element(By.CLASS_NAME,'heading-part')
    try: # Return empty dictionary if it's a premium story
        title_element.find_element(By.CLASS_NAME,'ie-premium')
        # print("Premium story")
        return {}
    except:
        pass
    try: # Return empty dictionary if it's a live blog
        title_element.find_element(By.CLASS_NAME,'livegif')
        # print("Title Missing")
        return {}
    except:
        pass
    try: # Search for a video link
        video_element = driver.find_element(By.CLASS_NAME,'ytp-impression-link')
        story['video_url'] = video_element.get_attribute('href')
    except:
        story['video_url'] = ''
    story['title'] = title_element.find_element(By.TAG_NAME,'h1').text
    story['description'] = title_element.find_element(By.TAG_NAME,'h2').text

    author_element = driver.find_element(By.CLASS_NAME,'editor')
    try: # If author is missing
        story['author'] = author_element.find_element(By.TAG_NAME,'a').text
    except:
        story['author'] = ''
    updated_timestamp = author_element.find_element(By.TAG_NAME, 'span').text
    # if 'Updated: ' in updated_timestamp:
    #     story['updated_timestamp'] = get_iso_datetime(updated_timestamp[9:], "%B %d, %Y %H:%M IST") # To remove Updated: 
    # else:
    #     story['updated_timestamp'] = get_iso_datetime(updated_timestamp, "%B %d, %Y %H:%M IST")
    try: # Search for the city
        story['city_name'] = author_element.find_element(By.TAG_NAME,'br').text
    except:
        story['city_name'] = ''


    content_element = driver.find_element(By.CLASS_NAME,'full-details')
    try: # If image is missing
        story['image_url'] = content_element.find_element(By.TAG_NAME,'img').get_attribute('src')
    except:
        story['image_url'] = ''
    try: # If content is missing, don't carry on with this story
        story['content'] = []
        count = 1
        for para_element in content_element.find_elements(By.TAG_NAME, 'p'):
            story['content'].append(para_element.text)
            # print(para_element.text, count)
            count += 1
        # story['content'] = story['content'][:-2] #This line was used when content was of type string to remove last '\n'.
    except:
        # print("Content Missing")
        return {}
    first_publish_element = driver.find_element(By.CLASS_NAME,'ie-first-publish')
    try: # If Published Timestamp is missing
        published_time = first_publish_element.find_element(By.TAG_NAME,'span').text
        print(published_time)
        story['published_timestamp'] = get_iso_datetime(published_time, "%B %d, %Y %H:%M IST")
    except:
        # print("Published Timestamp Missing")
        return {}
    try: # If tag is missing
        tags_element = driver.find_element(By.CLASS_NAME,'storytags')
        story['tags'] = []
        for tag_element in tags_element.find_elements(By.TAG_NAME,'li'):
            if 'tags' in tag_element.text.lower():
                continue
            story['tags'].append(tag_element.text)
    except:
        story['tags'] = []
    return story