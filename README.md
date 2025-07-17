# Keep-Alive Bot

Bot automatizado para manter sites hospedados no Render sempre ativos, evitando que entrem em modo "sleep" no plano gratuito.

## 🎯 Funcionalidades

- ✅ Monitora múltiplos sites simultaneamente
- ✅ Intervalo otimizado (14min 50s ± 2min) para planos gratuitos
- ✅ Sistema de logs completo (arquivo + console)
- ✅ Tratamento robusto de erros
- ✅ Headers realistas para simular navegador
- ✅ Intervalos randomizados para parecer tráfego natural

## 🚀 Como usar

### Localmente:

```bash
python keep_alive_bot.py
```

### Deploy no Render:

1. Crie um novo **Background Worker** no Render
2. Conecte este repositório
3. Configure o comando de start: `python keep_alive_bot.py`
4. Deploy automático será feito

## ⚙️ Configuração

Edite o arquivo `keep_alive_bot.py`:

```python
# Adicione suas URLs aqui:
URLS = [
    "https://seu-site.onrender.com",
    "https://outro-site.onrender.com",
]
```

## 📊 Logs

Os logs incluem:

- ✅ Sucessos (status 200)
- ⚠️ Falhas HTTP (4xx, 5xx)
- ⏰ Timeouts
- 🔌 Erros de conexão
- ❌ Erros inesperados

## 🌟 Estratégias para Sites Sempre Online

### 1. **Bot Keep-Alive (Esta solução)**

- Deploy do bot no Render como Background Worker
- O bot fica ativo 24/7 fazendo ping nos seus sites
- Custo: Gratuito (usa instância free do Render)

### 2. **Upgrade para Plano Pago**

- Render Pro ($7/mês): Sites nunca adormecem
- Mais confiável para aplicações críticas

### 3. **Serviços Externos de Monitoramento**

- UptimeRobot (gratuito para 50 monitores)
- Pingdom
- StatusCake

### 4. **Múltiplos Bots Distribuídos**

- Deploy em diferentes plataformas (Render, Railway, Fly.io)
- Redundância caso uma plataforma falhe

## 🎯 Recomendação

Para máxima eficiência:

1. **Deploy este bot no Render** como Background Worker
2. **Configure GitHub Actions** para auto-deploy
3. **Use UptimeRobot** como backup para monitorar tanto o bot quanto os sites
4. **Considere upgrade para Pro** se o projeto for comercial

## 📝 Notas Importantes

- Intervalo mínimo recomendado: 14 minutos
- Planos gratuitos dormem após 15 minutos de inatividade
- O bot consome poucos recursos (requests simples)
- Logs ajudam a debuggar problemas de conectividade
# keep_alive_bot
