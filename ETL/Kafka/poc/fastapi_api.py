from fastapi import FastAPI
import asyncio

from async_kafka_producer import send_msg

app = FastAPI()

@app.get("/")
async def read_root(query_param):
    asyncio.create_task(send_msg(query_param))
    return "sent"