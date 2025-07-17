#!/bin/bash

# Script para parar o bot
# Usage: ./stop_bot.sh

if [ -f "bot.pid" ]; then
    PID=$(cat bot.pid)
    echo "🛑 Parando bot com PID: $PID"
    kill $PID
    rm bot.pid
    echo "✅ Bot parado com sucesso!"
else
    echo "❌ Arquivo bot.pid não encontrado. O bot pode não estar rodando."
fi
