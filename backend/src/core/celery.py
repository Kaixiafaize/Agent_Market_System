import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# 初始化Celery
celery = Celery(
    "paper_tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

# 导入任务（后续celery worker启动时加载）
celery.autodiscover_tasks(["src.core.llm"])