# Bot de Backup - Versão simplificada e mais agressiva
import requests
import time
import logging
import random
from datetime import datetime

# Configuração mais agressiva para o backup
URLS_BACKUP = [
    "https://keep-alive-bot-tavl.onrender.com/health",  # Bot principal
    "https://dreamwalkerplane.onrender.com",            # Site alvo
]

# Intervalo menor para backup (10 minutos)
INTERVALO_BACKUP = 10 * 60
VARIACAO_BACKUP = 1 * 60  # ±1 minuto

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [BACKUP] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup_bot.log'),
        logging.StreamHandler()
    ]
)

def ping_site(url):
    """Função mais simples e rápida para ping"""
    headers = {
        "User-Agent": "KeepAlive-Backup/1.0",
        "Cache-Control": "no-cache"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        if 200 <= resposta.status_code < 300:
            logging.info(f"🔥 BACKUP - Ping OK: {url}")
            return True
        else:
            logging.warning(f"⚠️ BACKUP - Ping falhou ({resposta.status_code}): {url}")
            return False
    except Exception as e:
        logging.error(f"❌ BACKUP - Erro: {url} -> {e}")
        return False

def executar_backup():
    """Loop principal do bot backup"""
    logging.info("🔥 INICIANDO BOT DE BACKUP - MODO AGRESSIVO")
    logging.info(f"🎯 Alvos: {URLS_BACKUP}")
    
    ciclo = 0
    while True:
        ciclo += 1
        logging.info(f"🔄 [BACKUP] Ciclo #{ciclo}")
        
        for url in URLS_BACKUP:
            ping_site(url)
            time.sleep(3)  # Pausa curta entre pings
        
        # Intervalo randomizado
        intervalo = INTERVALO_BACKUP + random.randint(-VARIACAO_BACKUP, VARIACAO_BACKUP)
        logging.info(f"⏰ [BACKUP] Próximo ping em {intervalo//60}min {intervalo%60}s")
        time.sleep(intervalo)

if __name__ == "__main__":
    executar_backup()
