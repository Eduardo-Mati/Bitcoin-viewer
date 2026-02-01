from fastapi import APIRouter
import redis
import os
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
import io

import matplotlib
matplotlib.use('Agg')

router = APIRouter()

# Conecta no mesmo Redis que o robô está usando
REDIS_HOST = os.getenv("REDIS_HOST", "redis_db") # 'redis_db' é o nome no docker-compose
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@router.get("/price")
def get_bitcoin_price():
    # Tenta ler o valor que o robô gravou
    price = redis_client.get("btc_price")
    
    if price:
        return {"symbol": "BTC", "usd_price": float(price), "source": "Cache (Redis)"}
    
    return {"error": "Preço ainda não coletado pelo robô"}

@router.get("/chart")
def get_bitcoin_chart():
    # 1. Pega a lista de preços do Redis (do índice 0 ao fim)
    prices_str = redis_client.lrange("btc_history", 0, -1)
    
    # Converte de string para float (se não tiver dados, cria lista vazia)
    prices = [float(p) for p in prices_str] if prices_str else []

    # 2. Cria o Gráfico
    plt.figure(figsize=(10, 5)) # Tamanho da imagem
    plt.plot(prices, marker='o', linestyle='-', color='orange')
    plt.title("Histórico do Bitcoin (Últimas Leituras)")
    plt.xlabel("Tempo (leituras)")
    plt.ylabel("Preço (USD)")
    plt.grid(True)

    # 3. Salva a imagem na memória (buffer) em vez de salvar arquivo
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close() # Limpa a memória do gráfico

    # 4. Retorna a imagem como resposta
    return StreamingResponse(buf, media_type="image/png")