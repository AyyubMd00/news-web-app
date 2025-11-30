import azure.functions as func
import asyncio

from utils.async_kafka_producer import send_msg
from utils.sync_dwh import sync_dwh

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="KafkaProducer")
async def KafkaProducer(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "message: No Message Body!",
            status_code=400
        )

    asyncio.create_task(send_msg(req_body))
    return func.HttpResponse(
        "message: Message is being produced to the topic!",
        status_code=200
    )

@app.schedule(schedule="* */10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def SyncDWH(myTimer: func.TimerRequest) -> None:
    sync_dwh()