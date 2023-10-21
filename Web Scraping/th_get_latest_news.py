from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import sys

sys.path.append("Utils")
from th_get_full_story import get_full_story
from db_utils import upload_story_in_db, is_story_present_in_db
from get_category import get_category

chrome_options = Options()
# chrome_options.binary_location = 'selenium\chrome-win64\chrome.exe'
chrome_options.add_argument('--disable-clound-management') # To Remove an error not related to selenium
chrome_options.add_argument('--headless') # Headless Browser
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.thehindu.com/latest-news/')
print(driver.current_url)

driver.implicitly_wait(10)

latest_news_element = driver.find_element(By.CLASS_NAME,'latest-news')

for news_element in latest_news_element.find_elements(By.TAG_NAME, 'li'):
    category = news_element.find_elements(By.TAG_NAME, 'a')[1].text
    if category not in ['PREMIUM', 'SPONSORED CONTENT', 'NEWS']:
        link_element = news_element.find_element(By.TAG_NAME, 'a')
        link = link_element.get_attribute('href')
        try:
            link_element.find_element(By.CLASS_NAME, 'picture')
        except:
            print("continuing...")
            continue
        if is_story_present_in_db(link)==True:
            continue
        story = get_full_story(link)
        print(story)
        if story != {}:
            story['category'] = get_category(story['title'], story['description'])
            upload_story_in_db(story)