import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# 数据库连接
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# 创建所有表（首次启动时执行）
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 数据库会话依赖（供接口调用）
def get_db():
    with Session(engine) as session:
        yield session