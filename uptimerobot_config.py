# UptimeRobot - Configuração de Backup Externa
# Acesse: https://uptimerobot.com (50 monitores grátis)

# Sites para adicionar no UptimeRobot:
SITES_UPTIMEROBOT = [
    {
        "name": "DreamWalker Plane",
        "url": "https://dreamwalkerplane.onrender.com",
        "interval": 5,  # minutos
        "type": "HTTP"
    },
    {
        "name": "Keep-Alive Bot Principal",
        "url": "https://keep-alive-bot-tavl.onrender.com/health",
        "interval": 5,  # minutos
        "type": "HTTP"
    },
    # Adicione mais conforme necessário
]

# Configurações recomendadas:
# - Intervalo: 5 minutos
# - Timeout: 30 segundos
# - Alertas: Email quando down
# - Public Status Page: Opcional

print("📊 CONFIGURAÇÃO UPTIMEROBOT:")
for i, site in enumerate(SITES_UPTIMEROBOT, 1):
    print(f"{i}. {site['name']}")
    print(f"   URL: {site['url']}")
    print(f"   Intervalo: {site['interval']} min")
    print()
