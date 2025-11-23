from faststream.rabbit import RabbitBroker
from fastapi import Depends
from src.models.corrida_model import Corrida

broker = RabbitBroker("amqp://rabbitmq:5672")

async def publish_corrida_event(corrida: Corrida):
    await broker.publish(
        corrida.model_dump(),
        routing_key="corrida_finalizada"
    )
