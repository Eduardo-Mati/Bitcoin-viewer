import time
import requests
import redis
import os

# Pega o host do Redis do Docker Compose (ou localhost se for teste manual)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Conecta no Banco de Memória
# decode_responses=True faz o Redis já devolver string em vez de bytes
client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def fetch_price():
    try:
        # API gratuita da CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return None

print("🤖 Robô de Cripto INICIADO! Monitorando BTC...")

while True:
    while True:
        price = fetch_price()
        
        if price:
            print(f"💰 Bitcoin: ${price}")
            
            # 1. Adiciona o preço novo no FIM da lista 'btc_history'
            client.rpush("btc_history", price)
            
            # 2. Mantém apenas os últimos 50 preços (para não lotar a memória)
            client.ltrim("btc_history", -50, -1)
            
            # (Opcional) Mantém a chave antiga para consulta rápida
            client.set("btc_price", price)
        
        time.sleep(30)