from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import redis
import os
import matplotlib.pyplot as plt
import io
import matplotlib

# Configuração para rodar sem monitor (headless)
matplotlib.use('Agg')

router = APIRouter()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# ROTA DE PREÇO: Aceita /crypto/price/bitcoin ou /crypto/price/solana
@router.get("/price/{coin_id}")
def get_price(coin_id: str):
    # Tenta buscar a chave específica (ex: solana_price)
    price = redis_client.get(f"{coin_id}_price")
    
    if price:
        return {
            "id": coin_id,
            "name": coin_id.upper(),
            "usd_price": float(price)
        }
    
    return {"error": f"Moeda '{coin_id}' não encontrada ou robô ainda não coletou."}

# ROTA DE GRÁFICO: Aceita /crypto/chart/ethereum
@router.get("/chart/{coin_id}")
def get_chart(coin_id: str):
    # Busca o histórico específico (ex: ethereum_history)
    key = f"{coin_id}_history"
    prices_str = redis_client.lrange(key, 0, -1)
    
    # Converte para números
    prices = [float(p) for p in prices_str] if prices_str else []

    # Configura o visual do gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(prices, marker='o', linestyle='-', color='#facc15', linewidth=2) # Amarelo/Laranja
    
    plt.title(f"Histórico: {coin_id.upper()}")
    plt.ylabel("Preço (USD)")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Cor de fundo escura para combinar com seu Dashboard
    ax = plt.gca()
    ax.set_facecolor('#1e293b') # Cinza escuro
    plt.gcf().set_facecolor('#0f172a') # Fundo da borda

    # Salva na memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")