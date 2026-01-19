from fastapi import FastAPI
from routers import userRouter
from schemas import userSchema
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = FastAPI()

#para rodar o código use o comando: uvicorn main:app --reload

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    # Verifica a conexão
    client.admin.command('ping')
    print("Conectado ao MongoDB com sucesso!")
    db = client['seu_banco_dados']  # Substitua pelo nome do seu banco
except ServerSelectionTimeoutError:
    print("Erro: Não foi possível conectar ao MongoDB")
    client = None
except Exception as e:
    print(f"Erro na conexão: {e}")
    client = None


app.include_router(userRouter, prefix='/api/user')


