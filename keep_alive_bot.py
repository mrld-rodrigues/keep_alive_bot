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
    "https://dreamwalkerplane.onrender.com",
    # Adicione outras URLs aqui se necessário
    # "https://outro-site.onrender.com",
]

# Intervalo entre as requisições: 14 minutos e 50 segundos (em segundos)
# Com variação aleatória de ±2 minutos para parecer mais natural
INTERVALO_BASE = 14 * 60 + 50
VARIACAO_MAXIMA = 2 * 60  # ±2 minutos

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
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        # Envia uma requisição GET para a URL com timeout
        resposta = requests.get(url, headers=headers, timeout=TIMEOUT_REQUISICAO)

        # Se o site respondeu com sucesso (código 200)
        if resposta.status_code == 200:
            logging.info(f"✅ Acesso bem-sucedido ao site: {url}")
        else:
            # Se respondeu com outro código (ex: 503, 404, etc.)
            logging.warning(f"⚠️ Acesso com falha ({resposta.status_code}) ao site: {url}")

    except requests.exceptions.Timeout:
        logging.error(f"⏰ Timeout ao acessar o site: {url}")
    except requests.exceptions.ConnectionError:
        logging.error(f"🔌 Erro de conexão ao acessar o site: {url}")
    except Exception as e:
        # Em caso de erro (timeout, rede fora, etc.)
        logging.error(f"❌ Erro inesperado ao acessar {url}: {e}")

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
    iniciar_bot()
