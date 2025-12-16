#!/bin/bash
# 极简启动：Celery + FastAPI
export PYTHONPATH="/workspaces/Agent_Market_System/backend:$PYTHONPATH"
source /workspaces/Agent_Market_System/myenv/bin/activate
cd /workspaces/Agent_Market_System/backend || exit

# 杀残留进程
pkill -f "celery -A src.core.celery worker" >/dev/null 2>&1
pkill -f "python src/main.py" >/dev/null 2>&1

# 启动服务
celery -A src.core.celery worker --loglevel=info &
python src/main.py &

echo "服务已启动"