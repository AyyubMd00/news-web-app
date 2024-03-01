import logging
import azure.functions as func

from web_scraping.th_get_news import get_news as th_get_news
from web_scraping.ie_get_news import get_news as ie_get_news
from utils.get_category_and_tags import get_category_and_tags

app = func.FunctionApp()

@app.schedule(schedule="0 0,30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchNewsTH(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    th_get_news()
    logging.info('FetchNewsTH function executed.')

@app.timer_trigger(schedule="0 15,45 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchNewsIE(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    ie_get_news()
    logging.info('FetchNewsIE function executed.')

@app.timer_trigger(schedule="0 5,10,20,25,35,40,50,55 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def PredictCategory(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    get_category_and_tags()
    logging.info('PredictCategory function executed.')