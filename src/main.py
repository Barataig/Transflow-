from fastapi import FastAPI
from fastapi import Depends
from src.models.corrida_model import Corrida
from src.database.mongo_client import get_database
from src.database.redis_client import get_redis
from src.producer import publish_corrida_event

app = FastAPI()

@app.get("/")
def root():
    return {"status": "TransFlow API ativa!"}

@app.post("/corridas")
async def criar_corrida(corrida: Corrida, db=Depends(get_database)):
    await publish_corrida_event(corrida)
    return {"mensagem": "Corrida enviada para processamento"}

@app.get("/corridas")
async def listar_corridas(db=Depends(get_database)):
    corridas = await db.corridas.find().to_list(1000)
    return corridas

@app.get("/corridas/{forma_pagamento}")
async def filtrar_corridas(forma_pagamento: str, db=Depends(get_database)):
    corridas = await db.corridas.find({"forma_pagamento": forma_pagamento}).to_list(1000)
    return corridas

@app.get("/saldo/{motorista}")
async def saldo_motorista(motorista: str, redis=Depends(get_redis)):
    saldo = await redis.get(f"saldo:{motorista}")
    return {"motorista": motorista, "saldo": float(saldo or 0)}
