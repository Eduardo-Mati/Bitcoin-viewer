from motor.motor_asyncio import AsyncIOMotorClient
import os

# URL de conexão do MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "bitcoin"

# Cliente do MongoDB
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Coleções
users_collection = database["users"]

# Função para fechar conexão
async def close_mongo_connection():
    client.close()