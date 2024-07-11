"""
Queue Service Module

This service handles the receiving and sending of messages via a RabbitMQ implementation.
It will receive and process the messages added into the queue from the connector service.
"""

import asyncio
import aio_pika
import json
from expense_processor import process_expense
import os
from db.models.users import get_user, add_user, User
from dotenv import load_dotenv

load_dotenv()


OUTGOING_QUEUE = os.getenv('OUTGOING_QUEUE')
INCOMING_QUEUE = os.getenv('INCOMING_QUEUE')

async def receive_messages(pool):
    try:
        connection = await aio_pika.connect_robust(os.getenv('QUEUE_URL'))
        channel = await connection.channel()
        queue = await channel.declare_queue(INCOMING_QUEUE, durable=True)

        async def on_message(message: aio_pika.IncomingMessage):
            async with message.process():
                await process_message(pool, message.body.decode())

        await queue.consume(on_message)
        print('Waiting for messages...')
        await asyncio.Future()  # Run forever
    except Exception as e:
        print(f"Failed to set up consumer: {e}")
        await asyncio.sleep(5)  # Retry after delay
        await receive_messages(pool)

async def send_message(message):
    try:
        if message:
            connection = await aio_pika.connect_robust(os.getenv('QUEUE_URL'))
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue(OUTGOING_QUEUE, durable=True)
                await channel.default_exchange.publish(
                    aio_pika.Message(body=json.dumps(message).encode()),
                    routing_key=OUTGOING_QUEUE,
                )
                print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

async def process_message(pool, message):
    try:
        data = json.loads(message)
        telegram_id = data['chatId']
        text = data['text']

        user = await get_user(pool, str(telegram_id))
        
        if user is None:
            if text == '/register':
                await add_user(pool, User(id=None, telegram_id=str(telegram_id)))
                await send_message({'chatId': telegram_id, 'text': 'User succesfully registered'})
            else:
                await send_message({'chatId': telegram_id, 'text': 'User not registered, send /register to register into bot'})
        else:
            response = await process_expense(pool, text, user.id)
            if response:
                await send_message({'chatId':telegram_id, 'text': response})
    except Exception as e:
        print(f"Failed to process message: {e}")