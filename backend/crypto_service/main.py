import time
import requests
import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Lista de moedas que queremos monitorar (IDs do CoinGecko)
COINS = ["bitcoin", "ethereum", "solana"]

def fetch_prices():
    try:
        # Busca todas de uma vez separadas por vírgula
        ids = ",".join(COINS)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
        
        response = requests.get(url, timeout=5)
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return None

print(f"🤖 Robô INICIADO! Monitorando: {COINS}")

while True:
    data = fetch_prices()
    
    if data:
        for coin in COINS:
            if coin in data:
                price = data[coin]['usd']
                print(f"💰 {coin.upper()}: ${price}")
                
                # Salva com chaves dinâmicas: 'bitcoin_price', 'ethereum_price'...
                client.set(f"{coin}_price", price)
                
                # Salva histórico específico para cada moeda
                client.rpush(f"{coin}_history", price)
                client.ltrim(f"{coin}_history", -50, -1)
    
    time.sleep(30)