import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session
from src.api.auth import verify_api_key
from src.core.llm import generate_paper_task
from src.database.session import get_db
from src.model.paper_task import PaperTask

# 路由实例（注册到FastAPI主应用）
router = APIRouter(prefix="/papers", tags=["papers"])

# 1. 生成论文接口
@router.post("/generate", dependencies=[Depends(verify_api_key)])  # 去掉Depends则关闭鉴权
def create_paper(topic: str, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())
    # 创建任务记录
    db_task = PaperTask(id=task_id, topic=topic)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    # 提交Celery异步任务
    generate_paper_task.delay(task_id, topic)
    return {"task_id": task_id, "status": db_task.status}

# 2. 查询任务状态接口
@router.get("/{task_id}/status", dependencies=[Depends(verify_api_key)])
def get_task_status(task_id: str, db: Session = Depends(get_db)):
    task = db.get(PaperTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {
        "task_id": task.id,
        "topic": task.topic,
        "status": task.status,
        "created_at": task.created_at
    }

# 3. 下载PDF接口
@router.get("/{task_id}/download", dependencies=[Depends(verify_api_key)])
def download_paper(task_id: str, db: Session = Depends(get_db)):
    task = db.get(PaperTask, task_id)
    if not task or task.status != "completed" or not os.path.exists(task.file_path):
        raise HTTPException(status_code=400, detail="论文未生成或文件丢失")
    return FileResponse(
        path=task.file_path,
        filename=f"paper_{task_id}.pdf",
        media_type="application/pdf"
    )