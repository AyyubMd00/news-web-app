from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from ie_get_full_story import get_full_story
from db_utils import upload_story_in_db, is_story_present_in_db

    

chrome_options = Options()
# chrome_options.binary_location = 'selenium\chrome-win64\chrome.exe'
chrome_options.add_argument('--disable-clound-management') # To Remove an error not related to selenium
chrome_options.add_argument('--headless') # Headless Browser
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://indianexpress.com/section/cities/')
print(driver.current_url)

driver.implicitly_wait(10)

nation_element = driver.find_element(By.CLASS_NAME,'nation')

city_news_count = 0
for city_news_element in nation_element.find_elements(By.CLASS_NAME,'articles'):
    try:
        print("Element Tag:", city_news_element.tag_name, "Element ID:", city_news_element.id)
    except StaleElementReferenceException:
        # If the element is stale, re-fetch it
        nation_element = driver.find_element(By.CLASS_NAME,'nation')
        city_news_element = nation_element.find_elements(By.CLASS_NAME, 'articles')[city_news_count]
        print("Element Tag:", city_news_element.tag_name, "Element ID:", city_news_element.id)
    city_news_url = city_news_element.find_element(By.CLASS_NAME,'img-context').find_element(By.CLASS_NAME,'title').find_element(By.TAG_NAME,'a').get_attribute('href')
    city_news_count += 1
    if is_story_present_in_db(city_news_url)==True:
        continue
    print('News Count:',city_news_count)
    city_story = get_full_story(city_news_url, "cities", "india", "english")
    if city_story != {}:
        upload_story_in_db(city_story)

driver.quit()