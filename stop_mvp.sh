#!/bin/bash
# 极简停止：Celery + FastAPI
pkill -f "celery -A src.core.celery worker" >/dev/null 2>&1
pkill -f "python src/main.py" >/dev/null 2>&1
echo "服务已停止"