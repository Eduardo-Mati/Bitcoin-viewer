import time
import requests
import os
import json
import redis
from datetime import datetime, timezone
from pymongo import MongoClient

# Configuração do MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URL)
database = mongo_client["bitcoin"]
prices_collection = database["crypto_prices"]

# Configuração do Redis (cache)
REDIS_HOST = os.getenv("REDIS_HOST", "redis_db")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_URL = (os.getenv("REDIS_URL") or "").strip().strip('"').strip("'")
VALID_REDIS_SCHEMES = ("redis://", "rediss://", "unix://")
CACHE_PREFIX = os.getenv("CACHE_PREFIX", "bitcoin-viewer")


def build_cache_key(*parts: str) -> str:
    safe_parts = [str(part).strip().lower() for part in parts if str(part).strip()]
    return f"{CACHE_PREFIX}:{':'.join(safe_parts)}"


def create_redis_client() -> redis.Redis:
    base_kwargs = {
        "decode_responses": True,
        "socket_connect_timeout": 2,
        "socket_timeout": 2,
        "health_check_interval": 30,
    }

    if REDIS_URL and REDIS_URL.lower().startswith(VALID_REDIS_SCHEMES):
        return redis.Redis.from_url(REDIS_URL, **base_kwargs)

    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        **base_kwargs,
    )


redis_client = create_redis_client()

# As 3 moedas escolhidas (IDs exatos da CoinGecko)
COINS = ["bitcoin", "ethereum", "solana"]

def fetch_prices():
    try:
        # Transforma a lista em string: "bitcoin,ethereum,solana"
        ids_string = ",".join(COINS)
        
        # Pede tudo de uma vez para economizar requisições
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd"
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return None

print(f"🤖 Robô Iniciado! Monitorando: {COINS}")

while True:
    data = fetch_prices()
    
    if data:
        # Para cada moeda na nossa lista...
        for coin in COINS:
            if coin in data:
                price = data[coin]['usd']
                print(f"💰 {coin.upper()}: ${price}")

                # Salva preço atual e histórico (últimos 50) no MongoDB
                prices_collection.update_one(
                    {"coin": coin},
                    {
                        "$set": {
                            "coin": coin,
                            "latest_price": float(price),
                            "updated_at": datetime.now(timezone.utc),
                        },
                        "$push": {
                            "history": {
                                "$each": [float(price)],
                                "$slice": -50,
                            }
                        },
                    },
                    upsert=True,
                )

                coin_data = prices_collection.find_one(
                    {"coin": coin},
                    {"_id": 0, "latest_price": 1, "history": 1}
                )

                if coin_data:
                    try:
                        redis_client.setex(
                            build_cache_key("price", coin),
                            60,
                            json.dumps(
                                {
                                    "id": coin,
                                    "name": coin.upper(),
                                    "usd_price": float(coin_data.get("latest_price", price)),
                                }
                            ),
                        )
                        redis_client.setex(
                            build_cache_key("history", coin),
                            120,
                            json.dumps([float(p) for p in coin_data.get("history", [])]),
                        )
                    except Exception as e:
                        print(f"⚠️ Falha ao gravar cache Redis para {coin}: {e}")
    
    # Espera 30 segundos
    time.sleep(30)