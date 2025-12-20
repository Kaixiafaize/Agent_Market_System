#!/bin/bash
# 极简启动：Celery + FastAPI
export PYTHONPATH="/home/zjw/project/Agent_Market_System/backend:$PYTHONPATH"
source /home/zjw/project/Agent_Market_System/.venv/bin/activate
cd /home/zjw/project/Agent_Market_System/backend || exit

# 杀残留进程
pkill -f "celery -A src.core.celery worker" >/dev/null 2>&1
pkill -f "python src/main.py" >/dev/null 2>&1

# 启动服务
celery -A src.core.celery worker --loglevel=info &
python src/main.py &

echo "服务已启动"