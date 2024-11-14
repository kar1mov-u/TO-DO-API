from sqlmodel import SQLModel,Field,Relationship
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, List


class TasksBase(SQLModel):
    title: str =Field(index=True)
    description: str
    priority: int=Field(...,ge=0,le=10)
    completed:bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)  

class TasksDB(TasksBase,table =True):
    __tablename__="tasks"
    id: int | None = Field(default=None,primary_key=True)
    user_id: int = Field(foreign_key="users.id",nullable=False)
    user: Optional["UserDB"] = Relationship(back_populates="tasks")
    
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
    __tablename__ = "users"
    id: int | None= Field(default=None,primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tasks : List["TasksDB"] = Relationship(back_populates="user")
    
class UserLogin(SQLModel):
    email: EmailStr
    password: str
    
    
class UserResponse(SQLModel):
    id: int
    username:str
    email: str  
    created_at: datetime
    password: str
    
class ActivityDB(SQLModel,table=True):
    id: int | None=Field(default=None,primary_key=True)
    time: datetime=Field(default_factory=datetime.utcnow)
    task_id: int = Field(foreign_key="tasks.id",nullable=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    message: str = Field(nullable=False)
    user: "UserDB" = Relationship(back_populates="activities")  
    task: Optional["TasksDB"] = Relationship(back_populates="activities")  
    
    

    
    



