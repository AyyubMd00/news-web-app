import logging
import azure.functions as func
import requests

# sys.path.append("Web Scraping")
from web_scraping.ie_get_news import get_news as ie_get_news
from web_scraping.th_get_news import get_news as th_get_news
from utils.predict_category import predict_category
app = func.FunctionApp()
predict_category_function_url = 'https://func-news-app-process-news.azurewebsites.net/api/PredictCategory'

@app.schedule(schedule="0 0,30 * * * *", arg_name="myTimer",
              use_monitor=False) 
def FetchNews(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    th_get_news()
    
    requests.get(predict_category_function_url)
    logging.info('Python timer trigger function executed.')

@app.timer_trigger(schedule="0 15,45 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def FetchNewsIE(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    ie_get_news()
    requests.get(predict_category_function_url)
    logging.info('Python timer trigger function executed.')

@app.route(route="PredictCategory", auth_level=func.AuthLevel.ANONYMOUS)
def PredictCategory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    predict_category()
    
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )