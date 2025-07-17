from flask import Flask, jsonify
import threading
import time
import requests
import logging
from datetime import datetime
import random
import os

app = Flask(__name__)

# Configurações
URLS = [
    "https://dreamwalkerplane.onrender.com",
    "https://amiraldo-protifolio-flask-3.onrender.com"
]

INTERVALO_BASE = 14 * 60 + 50  # 14min 50s
VARIACAO_MAXIMA = 2 * 60  # ±2 minutos
TIMEOUT_REQUISICAO = 30

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Variáveis globais para status
status_bot = {
    "ativo": False,
    "ultimo_ciclo": None,
    "total_ciclos": 0,
    "sucessos": 0,
    "falhas": 0,
    "urls": URLS
}

def acessar_site(url):
    """Acessa um site específico"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_REQUISICAO)
        
        if resposta.status_code == 200:
            logging.info(f"✅ Sucesso: {url}")
            status_bot["sucessos"] += 1
            return True
        else:
            logging.warning(f"⚠️ Falha ({resposta.status_code}): {url}")
            status_bot["falhas"] += 1
            return False
            
    except Exception as e:
        logging.error(f"❌ Erro ao acessar {url}: {e}")
        status_bot["falhas"] += 1
        return False

def bot_worker():
    """Função que roda em thread separada"""
    logging.info("🚀 Iniciando Keep-Alive Bot em background")
    status_bot["ativo"] = True
    ciclo = 0
    
    while status_bot["ativo"]:
        ciclo += 1
        status_bot["total_ciclos"] = ciclo
        status_bot["ultimo_ciclo"] = datetime.now().isoformat()
        
        logging.info(f"🔄 Ciclo #{ciclo}")
        
        # Acessa todos os sites
        for url in URLS:
            acessar_site(url)
            time.sleep(5)  # Pausa entre sites
        
        # Calcula próximo intervalo
        intervalo = INTERVALO_BASE + random.randint(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
        logging.info(f"⏱️ Aguardando {intervalo//60}min {intervalo%60}s")
        
        time.sleep(intervalo)

# Inicia o bot em thread separada
bot_thread = threading.Thread(target=bot_worker, daemon=True)
bot_thread.start()

# Rotas da API
@app.route('/')
def home():
    return jsonify({
        "status": "Keep-Alive Bot Ativo",
        "message": "Bot funcionando em background",
        "endpoints": {
            "/status": "Status detalhado do bot",
            "/health": "Health check simples"
        }
    })

@app.route('/status')
def status():
    return jsonify(status_bot)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
