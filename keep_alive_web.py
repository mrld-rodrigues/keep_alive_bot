# Versão avançada do Keep-Alive Bot com servidor web para health check
# Use esta versão se quiser deployar no Render como Web Service

from flask import Flask, jsonify
import threading
import requests
import time
import logging
import random
import os
from datetime import datetime

app = Flask(__name__)

# =======================
# CONFIGURAÇÕES
# =======================

URLS = [
    "https://dreamwalkerplane.onrender.com",
    "https://amiraldo-protifolio-flask.onrender.com/"
    # Adicione outras URLs aqui
]

INTERVALO_BASE = 14 * 60 + 50  # 14min 50s
VARIACAO_MAXIMA = 2 * 60       # ±2 minutos
TIMEOUT_REQUISICAO = 30

# Status global do bot
bot_status = {
    "inicio": datetime.now(),
    "ultimo_ciclo": None,
    "ciclos_executados": 0,
    "sites_ok": 0,
    "sites_erro": 0,
    "proximo_ciclo": None
}

# =======================
# CONFIGURAÇÃO DE LOGS
# =======================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)

# =======================
# FUNÇÕES DO BOT
# =======================

def acessar_site(url):
    """Acessa um site específico."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_REQUISICAO)
        
        if resposta.status_code == 200:
            logging.info(f"✅ {url} - OK")
            bot_status["sites_ok"] += 1
            return True
        else:
            logging.warning(f"⚠️ {url} - Status {resposta.status_code}")
            bot_status["sites_erro"] += 1
            return False
            
    except requests.exceptions.Timeout:
        logging.error(f"⏰ {url} - Timeout")
        bot_status["sites_erro"] += 1
        return False
    except requests.exceptions.ConnectionError:
        logging.error(f"🔌 {url} - Erro de conexão")
        bot_status["sites_erro"] += 1
        return False
    except Exception as e:
        logging.error(f"❌ {url} - Erro: {e}")
        bot_status["sites_erro"] += 1
        return False

def executar_ciclo():
    """Executa um ciclo completo de verificação."""
    bot_status["ultimo_ciclo"] = datetime.now()
    bot_status["ciclos_executados"] += 1
    
    logging.info(f"🔄 Ciclo #{bot_status['ciclos_executados']}")
    
    for url in URLS:
        acessar_site(url)
        if len(URLS) > 1:
            time.sleep(5)  # Pausa entre sites

def bot_worker():
    """Worker thread que executa o bot."""
    logging.info("🚀 Keep-Alive Bot iniciado")
    logging.info(f"📊 Monitorando {len(URLS)} site(s)")
    
    while True:
        executar_ciclo()
        
        # Calcula próximo ciclo
        intervalo = INTERVALO_BASE + random.randint(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
        bot_status["proximo_ciclo"] = datetime.now().timestamp() + intervalo
        
        logging.info(f"⏱️ Aguardando {intervalo//60}min {intervalo%60}s...")
        time.sleep(intervalo)

# =======================
# ROTAS WEB (HEALTH CHECK)
# =======================

@app.route('/')
def health_check():
    """Endpoint de health check para o Render."""
    return jsonify({
        "status": "healthy",
        "bot_rodando": True,
        "inicio": bot_status["inicio"].isoformat(),
        "ultimo_ciclo": bot_status["ultimo_ciclo"].isoformat() if bot_status["ultimo_ciclo"] else None,
        "ciclos_executados": bot_status["ciclos_executados"],
        "sites_monitorados": len(URLS),
        "sites_ok": bot_status["sites_ok"],
        "sites_erro": bot_status["sites_erro"],
        "proximo_ciclo": bot_status["proximo_ciclo"]
    })

@app.route('/status')
def status_detalhado():
    """Status detalhado do bot."""
    agora = datetime.now().timestamp()
    tempo_para_proximo = max(0, (bot_status["proximo_ciclo"] or agora) - agora)
    
    return jsonify({
        "bot": {
            "status": "rodando",
            "uptime_segundos": (datetime.now() - bot_status["inicio"]).total_seconds(),
            "ciclos_executados": bot_status["ciclos_executados"],
            "ultimo_ciclo": bot_status["ultimo_ciclo"].isoformat() if bot_status["ultimo_ciclo"] else None,
            "proximo_ciclo_em": f"{tempo_para_proximo//60:.0f}min {tempo_para_proximo%60:.0f}s"
        },
        "sites": {
            "total": len(URLS),
            "urls": URLS,
            "sucessos": bot_status["sites_ok"],
            "erros": bot_status["sites_erro"]
        },
        "config": {
            "intervalo_base": f"{INTERVALO_BASE//60}min {INTERVALO_BASE%60}s",
            "variacao": f"±{VARIACAO_MAXIMA//60}min"
        }
    })

# =======================
# INICIALIZAÇÃO
# =======================

if __name__ == "__main__":
    # Inicia o bot worker em thread separada
    bot_thread = threading.Thread(target=bot_worker, daemon=True)
    bot_thread.start()
    
    # Inicia o servidor web
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
