#!/bin/bash

pkill -f tgbot.py
sleep 2

PIDS=$(pgrep -f tgbot.py)
if [ -n "$PIDS" ]; then
  echo "Принудительное завершение процессов: $PIDS"
  kill -9 $PIDS
fi

echo "Процесс tgbot.py остановлен."