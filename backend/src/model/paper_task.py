from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class PaperTask(SQLModel, table=True):
    __tablename__ = "paper_tasks"
    id: str = Field(primary_key=True, index=True)
    topic: str = Field(index=True)
    status: str = Field(default="pending")
    file_path: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)