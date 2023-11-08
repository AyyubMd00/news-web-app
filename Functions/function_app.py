import logging
import azure.functions as func
# import sys

# sys.path.append("Web Scraping")
from web_scraping.ie_get_city_news import get_city_news
from web_scraping.th_get_latest_news import get_latest_news
app = func.FunctionApp()

@app.schedule(schedule="0 0,30 * * * *", arg_name="myTimer",
              use_monitor=False) 
def FetchNews(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    get_latest_news()
    print('Function has run')
    logging.info('Both functions executed.')

@app.timer_trigger(schedule="0 15,45 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def FetchNewsIE(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    get_city_news()
    logging.info('Python timer trigger function executed.')