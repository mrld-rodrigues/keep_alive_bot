# Importa bibliotecas necessárias
import requests  # Para fazer requisições HTTP
import time      # Para controlar os intervalos de tempo
import logging   # Para registrar mensagens em log (arquivo e terminal)
import os        # Para variáveis de ambiente
import random    # Para randomizar intervalos

# =======================
# CONFIGURAÇÕES PRINCIPAIS
# =======================

# URLs dos sites que serão mantidos ativos (suporte a múltiplos sites)
URLS = [
    # Sites principais - ESTRATÉGIA BIDIRECIONAL
    "https://dreamwalkerplane.onrender.com",
    "https://amiraldo-protifolio-flask.onrender.com/",  # Confirme se esta URL está correta
    
    # Auto-ping para manter o próprio bot ativo
    "https://keep-alive-bot-tavl.onrender.com/health",
    
    # Serviços externos para garantir conectividade
    "https://httpbin.org/status/200",
]

# Intervalo otimizado: 12 minutos (mais agressivo para garantir que não durma)
# O dreamwalker vai chamar o bot em intervalos diferentes para criar redundância
INTERVALO_BASE = 12 * 60  # 12 minutos
VARIACAO_MAXIMA = 1 * 60  # ±1 minuto

# Timeout para requisições (em segundos)
TIMEOUT_REQUISICAO = 30

# =======================
# CONFIGURAÇÃO DO SISTEMA DE LOGS
# =======================

# Cria o logger principal
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Define o nível de mensagens a registrar

# === Log em arquivo ===
file_handler = logging.FileHandler('keep_alive.log')  # Cria arquivo de log
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Formato do log
logger.addHandler(file_handler)  # Adiciona esse manipulador ao logger

# === Log no terminal (console) ===
console_handler = logging.StreamHandler()  # Saída no terminal
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Mesmo formato
logger.addHandler(console_handler)  # Adiciona esse manipulador ao logger

# =======================
# FUNÇÃO: Acessar o site
# =======================

def acessar_site(url):
    """
    Função responsável por acessar uma URL específica e registrar o status.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    try:
        # Envia uma requisição GET para a URL com timeout
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_REQUISICAO)

        # Se o site respondeu com sucesso (código 200-299)
        if 200 <= resposta.status_code < 300:
            logging.info(f"✅ Acesso bem-sucedido ao site: {url} (Status: {resposta.status_code})")
            return True
        else:
            # Se respondeu com outro código (ex: 503, 404, etc.)
            logging.warning(f"⚠️ Acesso com falha ({resposta.status_code}) ao site: {url}")
            return False

    except requests.exceptions.Timeout:
        logging.error(f"⏰ Timeout ao acessar o site: {url}")
        return False
    except requests.exceptions.ConnectionError:
        logging.error(f"🔌 Erro de conexão ao acessar o site: {url}")
        return False
    except Exception as e:
        # Em caso de erro (timeout, rede fora, etc.)
        logging.error(f"❌ Erro inesperado ao acessar {url}: {e}")
        return False

def acessar_todos_os_sites():
    """
    Acessa todos os sites da lista URLS.
    """
    for url in URLS:
        acessar_site(url)
        # Pequena pausa entre sites para não sobrecarregar
        if len(URLS) > 1:
            time.sleep(5)

# =======================
# FUNÇÃO PRINCIPAL DO BOT
# =======================

def iniciar_bot():
    """
    Função principal que inicia o bot e executa o loop infinito.
    """
    logging.info("🚀 Iniciando o Keep-Alive Bot")
    logging.info(f"📊 Monitorando {len(URLS)} site(s)")
    
    for i, url in enumerate(URLS, 1):
        logging.info(f"  {i}. {url}")

    # Loop infinito: acessa os sites e aguarda o tempo especificado
    ciclo = 0
    while True:
        ciclo += 1
        logging.info(f"🔄 Iniciando ciclo #{ciclo}")
        
        acessar_todos_os_sites()
        
        # Calcula intervalo com variação aleatória para parecer mais natural
        intervalo = INTERVALO_BASE + random.randint(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
        
        logging.info(f"⏱️ Aguardando {intervalo//60}min {intervalo%60}s até próximo ciclo...")
        time.sleep(intervalo)

# =======================
# EXECUÇÃO DO SCRIPT
# =======================

if __name__ == "__main__":
    # Verifica se está rodando no Render como Web Service
    import os
    if os.environ.get('PORT'):
        # Modo Web Service - inicia servidor Flask
        from flask import Flask, jsonify, request
        import threading
        from datetime import datetime
        
        app = Flask(__name__)
        
        # Status global
        bot_status = {
            "ativo": False,
            "ultimo_ciclo": None,
            "total_ciclos": 0,
            "urls": URLS
        }
        
        def bot_worker():
            """Roda o bot em thread separada"""
            bot_status["ativo"] = True
            ciclo = 0
            
            while bot_status["ativo"]:
                ciclo += 1
                bot_status["total_ciclos"] = ciclo
                bot_status["ultimo_ciclo"] = datetime.now().isoformat()
                
                logging.info(f"🔄 Iniciando ciclo #{ciclo}")
                acessar_todos_os_sites()
                
                intervalo = INTERVALO_BASE + random.randint(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
                logging.info(f"⏱️ Aguardando {intervalo//60}min {intervalo%60}s até próximo ciclo...")
                time.sleep(intervalo)
        
        @app.route('/')
        def home():
            return jsonify({
                "status": "Keep-Alive Bot Ativo",
                "strategy": "Bidirecional com DreamWalker",
                "bot_ativo": bot_status["ativo"],
                "total_ciclos": bot_status["total_ciclos"],
                "ultimo_ciclo": bot_status["ultimo_ciclo"],
                "urls_monitoradas": bot_status["urls"]
            })
        
        @app.route('/health')
        def health():
            return jsonify({
                "status": "ok", 
                "timestamp": datetime.now().isoformat(),
                "message": "Bot funcionando - DreamWalker pode me manter ativo!"
            })
        
        @app.route('/ping')
        def ping():
            """Endpoint especial para receber pings do DreamWalker"""
            source = request.headers.get('X-Source', 'unknown')
            logging.info(f"📡 Ping recebido de: {source}")
            return jsonify({
                "pong": True,
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "bot_status": "active"
            })
        
        # Inicia bot em thread separada
        bot_thread = threading.Thread(target=bot_worker, daemon=True)
        bot_thread.start()
        
        # Inicia servidor web
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Modo Background Worker - apenas o bot
        iniciar_bot()
