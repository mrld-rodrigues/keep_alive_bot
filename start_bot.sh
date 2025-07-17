#!/bin/bash

# Script para executar o bot localmente em background
# Usage: ./start_bot.sh

echo "🚀 Iniciando Keep-Alive Bot..."

# Instala dependências se necessário
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Inicia o bot em background
echo "🔄 Iniciando bot em background..."
nohup python keep_alive_bot.py > bot.log 2>&1 &

# Salva o PID do processo
echo $! > bot.pid

echo "✅ Bot iniciado com PID: $(cat bot.pid)"
echo "📋 Para ver logs: tail -f bot.log"
echo "🛑 Para parar: ./stop_bot.sh"
