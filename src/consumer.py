from faststream.rabbit import RabbitBroker
from src.database.mongo_client import get_database
from src.database.redis_client import get_redis

broker = RabbitBroker("amqp://rabbitmq:5672")

@broker.subscriber("corrida_finalizada")
async def process_corrida_event(event: dict):
    db = await get_database()
    redis = await get_redis()

    motorista = event["motorista"]["nome"]
    valor = float(event["valor_corrida"])

    # Atualiza saldo do motorista no Redis
    await redis.incrbyfloat(f"saldo:{motorista}", valor)

    # Salva corrida no MongoDB
    await db.corridas.insert_one(event)
