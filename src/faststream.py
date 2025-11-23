import json
import os
from aio_pika import connect_robust, Message, ExchangeType
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
QUEUE_NAME = os.getenv("QUEUE_NAME")

class FastStream:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        if self.connection is None:
            self.connection = await connect_robust(RABBITMQ_URL)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                EXCHANGE_NAME, ExchangeType.FANOUT
            )

    async def publish(self, routing_key: str, payload: dict):
        await self.connect()
        body = json.dumps(payload).encode()
        message = Message(body)
        await self.exchange.publish(message, routing_key=routing_key)

    async def consume(self, callback):
        await self.connect()
        queue = await self.channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.bind(self.exchange)

        async with queue.iterator() as iterator:
            async for message in iterator:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    await callback(payload)

faststream = FastStream()

async def publish(routing_key, payload):
    await faststream.publish(routing_key, payload)

async def consume(callback):
    await faststream.consume(callback)
