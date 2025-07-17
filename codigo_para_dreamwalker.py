# ====================================================
# CÓDIGO SIMPLES PARA ADICIONAR NO DREAMWALKER
# ====================================================
# Cole este código no seu projeto dreamwalkerplane.onrender.com

import threading
import time
import requests
import logging

def manter_bot_ativo():
    """Mantém o keep-alive-bot sempre acordado"""
    BOT_URL = "https://keep-alive-bot-tavl.onrender.com/health"
    
    def worker():
        ping_count = 0
        while True:
            ping_count += 1
            try:
                response = requests.get(BOT_URL, timeout=30)
                if response.status_code == 200:
                    logging.info(f"🤖 Bot #{ping_count}: ✅ ATIVO")
                else:
                    logging.warning(f"🤖 Bot #{ping_count}: ⚠️ Status {response.status_code}")
            except Exception as e:
                logging.error(f"🤖 Bot #{ping_count}: ❌ {e}")
            
            time.sleep(8 * 60)  # 8 minutos
    
    # Inicia em background
    threading.Thread(target=worker, daemon=True).start()
    logging.info("🚀 Sistema Keep-Alive iniciado!")

# ====================================================
# INSTRUÇÕES DE USO:
# ====================================================

# 1. Cole este código no seu arquivo principal do dreamwalker
# 2. Chame manter_bot_ativo() no início da sua aplicação
# 3. Exemplo:

"""
# No seu app.py ou main.py do dreamwalker:

from flask import Flask
import logging

# ... seu código existente ...

# ADICIONAR ESTAS LINHAS:
import threading
import time
import requests

def manter_bot_ativo():
    BOT_URL = "https://keep-alive-bot-tavl.onrender.com/health"
    def worker():
        ping_count = 0
        while True:
            ping_count += 1
            try:
                response = requests.get(BOT_URL, timeout=30)
                logging.info(f"🤖 Bot #{ping_count}: {'✅' if response.status_code == 200 else '⚠️'}")
            except Exception as e:
                logging.error(f"🤖 Bot #{ping_count}: ❌ {e}")
            time.sleep(8 * 60)
    threading.Thread(target=worker, daemon=True).start()

# Chamar no início:
manter_bot_ativo()

# ... resto do seu código ...
"""
