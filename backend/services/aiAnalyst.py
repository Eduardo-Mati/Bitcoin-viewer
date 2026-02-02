import google.generativeai as genai
import os

# Pega a chave do docker-compose ou .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def analyze_market_trend(coin_name, prices_list):
    if not GOOGLE_API_KEY:
        return "Erro: Chave da API do Google não configurada."

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # O modelo 'gemini-1.5-flash' é ótimo para tarefas rápidas e é free tier
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Transforma lista de números em texto
        prices_str = ", ".join([str(p) for p in prices_list])
        
        prompt = f"""
        Aja como um analista de criptomoedas experiente (estilo Day Trader).
        
        Dados recentes do {coin_name.upper()} (últimos candles de 30s):
        [{prices_str}]
        
        Tarefa:
        1. Qual é a tendência IMEDIATA? (Alta, Baixa ou Lateral)
        2. Dê uma recomendação curta (Compra, Venda ou Aguardar).
        3. Explique o motivo em 1 frase baseada nos números.
        4. diga o timeframe usado (ex: candles de 30s).
        
        Responda em Português, texto corrido, curto e direto. Sem formatação markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Erro no Gemini: {e}")
        return "IA indisponível no momento. Tente novamente."