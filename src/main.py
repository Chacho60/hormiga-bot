"""
Main Module

This module initializes the async connection pool and starts the message 
receiving service. It will check pool connections constantly to see if 
there are any dropped connections.
"""

import asyncio
from queue_service import receive_messages
from db.database import get_async_pool

async def init():
    try:
        async_pool = await get_async_pool()

        async def check_pool_connections():
            while True:
                await asyncio.sleep(600)
                print("check async connections")
                await async_pool.check()

        await asyncio.gather(
            receive_messages(async_pool),
            check_pool_connections()
        )
    except Exception as e:
        print(f"Failed to initialize service: {e}")

if __name__ == "__main__":
    asyncio.run(init())