from web_scraping.ie_get_news import get_news
# from web_scraping.ie_get_city_news import get_city_news
from web_scraping.ie_get_story import get_story
# from web_scraping.ie_get_full_story import get_full_story
# from web_scraping.th_get_news import get_news
# from web_scraping.th_get_story import get_story
from pprint import pprint
from datetime import datetime

# from web_scraping.th_get_latest_news import get_latest_news
from utils.get_category_bert import get_category
from utils.predict_category import predict_category

start_time = datetime.now()
print(start_time)
title = "Man thrashed and sexually assaulted in Delhi; police arrest 2"
description = "The incident took place on Diwali night when the complainant and the family of the accused were celebrating the festival."
print(get_category(title, description))
predict_category()
# get_news()
# get_city_news()
# print(get_story('https://www.thehindu.com/sport/cricket/captaincy-has-not-been-a-burden-for-me-babar-azam/article67522001.ece'))
# pprint(get_story('https://indianexpress.com/article/cities/pune/building-pune-cards-food-court-walking-plaza-saras-baug-9019975/'))
# pprint(get_full_story('https://indianexpress.com/article/cities/pune/building-pune-cards-food-court-walking-plaza-saras-baug-9019975/'))
# get_latest_news()
end_time = datetime.now()
print(end_time)
print(end_time - start_time)

