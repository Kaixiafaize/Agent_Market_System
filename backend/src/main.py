import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.api.paper import router as paper_router
from src.database.session import create_db_and_tables

load_dotenv()

# --------------------------
# 新增：lifespan 生命周期函数
# --------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行（替代原来的 startup 事件）
    create_db_and_tables()
    yield  # 应用运行中
    # 关闭时执行（可选，替代原来的 shutdown 事件）
    # 例如：关闭数据库连接、清理资源等
    pass

# 初始化FastAPI时绑定lifespan
app = FastAPI(title="Paper Generator MVP", lifespan=lifespan)

# 1. 配置CORS（允许前端跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 注册路由
app.include_router(paper_router)

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))