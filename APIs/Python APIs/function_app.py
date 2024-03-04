import azure.functions as func
import asyncio

from utils.async_kafka_producer import send_msg

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