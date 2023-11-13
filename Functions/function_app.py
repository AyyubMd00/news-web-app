import logging
import azure.functions as func
# import sys

# sys.path.append("Web Scraping")
from web_scraping.ie_get_news import get_news as ie_get_news
from web_scraping.th_get_news import get_news as th_get_news
app = func.FunctionApp()

@app.schedule(schedule="0 0,30 * * * *", arg_name="myTimer",
              use_monitor=False) 
def FetchNews(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    th_get_news()
    logging.info('Python timer trigger function executed.')

@app.timer_trigger(schedule="0 15,45 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchNewsIE(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    ie_get_news()
    logging.info('Python timer trigger function executed.')