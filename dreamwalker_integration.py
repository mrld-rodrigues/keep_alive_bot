# ============================================
# CÓDIGO PARA ADICIONAR NO DREAMWALKER PLANE
# ============================================

# Este código deve ser adicionado no seu projeto dreamwalkerplane.onrender.com
# para manter o keep-alive-bot sempre ativo

import threading
import time
import requests
import logging
from datetime import datetime

# ===== CONFIGURAÇÕES DO KEEP-ALIVE =====
BOT_URL = "https://keep-alive-bot-tavl.onrender.com/health"
INTERVALO_PING_BOT = 8 * 60  # 8 minutos (mais agressivo que o bot)

def ping_keep_alive_bot():
    """
    Função para manter o keep-alive-bot sempre ativo
    """
    headers = {
        "User-Agent": "DreamWalker-KeepAlive/1.0",
        "X-Source": "dreamwalkerplane"
    }
    
    try:
        response = requests.get(BOT_URL, headers=headers, timeout=30)
        if response.status_code == 200:
            logging.info(f"🤖 Bot keep-alive: SUCCESS (Status: {response.status_code})")
            return True
        else:
            logging.warning(f"🤖 Bot keep-alive: FAIL (Status: {response.status_code})")
            return False
    except Exception as e:
        logging.error(f"🤖 Bot keep-alive: ERROR - {e}")
        return False

def start_keep_alive_worker():
    """
    Inicia o worker que mantém o bot ativo
    Chame esta função no início da sua aplicação
    """
    def worker():
        logging.info("🚀 Iniciando Keep-Alive Worker para o Bot")
        ping_count = 0
        
        while True:
            ping_count += 1
            logging.info(f"🔄 Ping #{ping_count} para o Keep-Alive Bot")
            
            success = ping_keep_alive_bot()
            
            if success:
                logging.info(f"✅ Bot mantido ativo com sucesso")
            else:
                logging.error(f"❌ Falha ao manter bot ativo - tentando novamente em 2min")
                time.sleep(2 * 60)  # Tenta novamente em 2 minutos se falhar
                continue
            
            # Aguarda o intervalo normal
            logging.info(f"⏱️ Próximo ping em {INTERVALO_PING_BOT//60} minutos")
            time.sleep(INTERVALO_PING_BOT)
    
    # Inicia em thread separada para não bloquear a aplicação
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    logging.info("🎯 Keep-Alive Worker iniciado em background")

# ===== COMO USAR NO SEU PROJETO =====

# 1. Adicione este import no topo do seu arquivo principal:
# from keep_alive_integration import start_keep_alive_worker

# 2. Chame esta função no início da sua aplicação (após configurar logging):
# start_keep_alive_worker()

# 3. Exemplo de integração com Flask:
"""
from flask import Flask
import logging
from keep_alive_integration import start_keep_alive_worker

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Iniciar keep-alive worker
start_keep_alive_worker()

@app.route('/')
def home():
    return "DreamWalker Plane - Keep-Alive System Active!"

if __name__ == '__main__':
    app.run()
"""

# 4. Exemplo de integração com qualquer aplicação Python:
"""
import logging
from keep_alive_integration import start_keep_alive_worker

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Iniciar keep-alive worker
start_keep_alive_worker()

# Resto da sua aplicação...
"""
