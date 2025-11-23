import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "transflow")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

async def get_database():
    return db
