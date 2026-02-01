import time
import requests
import redis
import os

# Configuração do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

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
                
                # 1. Salva o preço atual: 'bitcoin_price', 'solana_price'...
                client.set(f"{coin}_price", price)
                
                # 2. Salva no histórico específico: 'bitcoin_history', 'solana_history'...
                history_key = f"{coin}_history"
                client.rpush(history_key, price)
                client.ltrim(history_key, -50, -1) # Mantém só os últimos 50
    
    # Espera 30 segundos
    time.sleep(30)