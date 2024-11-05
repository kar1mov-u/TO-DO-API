from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime


class TasksBase(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    title: str =Field(index=True)
    description: str
    priority: int=Field(...,ge=0,le=10)
    completed:bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)    

class TasksUpdate(SQLModel):
    title: Optional[str]    = None
    description: Optional[str] =None
    priority: Optional[int]=Field(None,ge=0,le=10)
    completed:Optional[bool] = None
