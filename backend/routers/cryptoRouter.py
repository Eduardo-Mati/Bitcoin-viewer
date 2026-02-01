from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import redis
import os
import matplotlib.pyplot as plt
import io
import matplotlib

matplotlib.use('Agg')

router = APIRouter()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Agora aceitamos o {coin_id} na URL
@router.get("/price/{coin_id}")
def get_crypto_price(coin_id: str):
    # Busca pela chave dinâmica (ex: ethereum_price)
    price = redis_client.get(f"{coin_id}_price")
    
    if price:
        return {"symbol": coin_id.upper(), "usd_price": float(price)}
    
    return {"error": "Moeda não encontrada ou ainda não coletada"}

@router.get("/chart/{coin_id}")
def get_crypto_chart(coin_id: str):
    # Busca histórico dinâmico (ex: ethereum_history)
    prices_str = redis_client.lrange(f"{coin_id}_history", 0, -1)
    prices = [float(p) for p in prices_str] if prices_str else []

    plt.figure(figsize=(10, 5))
    # Título dinâmico
    plt.title(f"Histórico de {coin_id.upper()}") 
    plt.plot(prices, marker='o', linestyle='-', color='orange')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")