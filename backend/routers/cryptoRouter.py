from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import os
import io
from pymongo import MongoClient
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from services.aiAnalyst import analyze_market_trend
from services.cache import build_cache_key, cache_get_json, cache_set_json




router = APIRouter()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URL)
database = mongo_client["bitcoin"]
prices_collection = database["crypto_prices"]


def _load_history(coin_id: str):
    history_cache_key = build_cache_key("history", coin_id)
    cached_history = cache_get_json(history_cache_key)

    if isinstance(cached_history, list):
        return [float(p) for p in cached_history]

    coin_data = prices_collection.find_one(
        {"coin": coin_id},
        {"_id": 0, "history": 1}
    )
    prices = [float(p) for p in coin_data.get("history", [])] if coin_data else []
    cache_set_json(history_cache_key, prices, ttl_seconds=120)
    return prices

# ROTA DE PREÇO: Aceita /crypto/price/bitcoin ou /crypto/price/solana
@router.get("/price/{coin_id}")
def get_price(coin_id: str):
    coin_id = coin_id.lower()
    price_cache_key = build_cache_key("price", coin_id)

    cached_price = cache_get_json(price_cache_key)
    if cached_price and cached_price.get("usd_price") is not None:
        return {
            "id": coin_id,
            "name": coin_id.upper(),
            "usd_price": float(cached_price["usd_price"])
        }

    coin_data = prices_collection.find_one(
        {"coin": coin_id},
        {"_id": 0, "latest_price": 1}
    )

    if coin_data and coin_data.get("latest_price") is not None:
        response = {
            "id": coin_id,
            "name": coin_id.upper(),
            "usd_price": float(coin_data["latest_price"])
        }
        cache_set_json(price_cache_key, response, ttl_seconds=60)
        return response
    
    return {"error": f"Moeda '{coin_id}' não encontrada ou robô ainda não coletou."}

# ROTA DE GRÁFICO: Aceita /crypto/chart/ethereum
@router.get("/chart/{coin_id}")
def get_chart(coin_id: str):
    coin_id = coin_id.lower()
    prices = _load_history(coin_id)

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

@router.get("/analyze/{coin_id}")
def get_ai_analysis(coin_id: str):
    coin_id = coin_id.lower()
    prices = _load_history(coin_id)

    if not prices:
        return {"analysis": "Dados insuficientes."}

    # Pega os últimos 30 preços
    prices = prices[-30:]
    
    # Chama o Gemini
    analysis_text = analyze_market_trend(coin_id, prices)
    
    return {
        "coin": coin_id, 
        "analysis": analysis_text,
        "source": "Google Gemini (Free Tier)"
    }