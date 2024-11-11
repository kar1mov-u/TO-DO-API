from sqlmodel import SQLModel,Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class TasksBase(SQLModel):
    title: str =Field(index=True)
    description: str
    priority: int=Field(...,ge=0,le=10)
    completed:bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)  

class TasksDB(TasksBase,table =True):
    id: int | None = Field(default=None,primary_key=True)
    
class TasksUpdate(SQLModel):
    title: Optional[str]    = None
    description: Optional[str] =None
    priority: Optional[int]=Field(None,ge=0,le=10)
    completed:Optional[bool] = None
    
    
class UserBase(SQLModel):
    username: str =Field(nullable=False,unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(nullable=False)
    
class UserDB(UserBase,table=True):
    id: int | None= Field(default=None,primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserResponse(SQLModel):
    id: int
    username:str
    email: str
    created_at: datetime
    password: str
    
    



