import asyncio

async def long_running_task():
    await asyncio.sleep(10)
    print("completed")

async def main():
    asyncio.create_task(long_running_task())
    print("coroutine started")

asyncio.run(main())