import json, os, asyncio
import aio_pika
from app.core.config import RABBITMQ_URL

async def publish_event(event_type: str, payload: dict):
    try:
        conn = await aio_pika.connect_robust(RABBITMQ_URL)
        async with conn:
            channel = await conn.channel()
            exchange = channel.default_exchange
            message = aio_pika.Message(body=json.dumps({'event': event_type, 'data': payload}).encode())
            await exchange.publish(message, routing_key='webhook_events')
    except Exception as e:
        print('Failed publish_event', e)
