from passlib.context import CryptContext
from fastapi import HTTPException
from .database import SessionDep
from sqlmodel import select
from .models.sql_models import UserDB,ActivityDB
pwd_context =  CryptContext(schemes=['bcrypt'], deprecated="auto")

def hashing_pass(plain_pass):
    return pwd_context.hash(plain_pass)

def verify_pass(hashed_pass,plain_pass):
    return pwd_context.verify(plain_pass,hashed_pass)

def authenticate_user(session,email,password):
    user = session.exec(select(UserDB).where(UserDB.email==email)).first()
    if not user:
        return False
    if not verify_pass(user.password,password):
        return False
    return user

def get_current_user_object(session,email):
    user =session.exec(select(UserDB).where(UserDB.email==email)).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid user")
    return user

def validate_user_to_task(user_id, task_user_id):
    if user_id!=task_user_id:
        raise HTTPException(status_code=404, detail="THis task does not belong to you")
    
    
    
def log_activity(session,user_id, message,task_id=None):
    try:
        log = ActivityDB()
        log.task_id = task_id
        log.user_id = user_id
        log.message = message
        session.add(log)
        session.commit()
        return True
    except:
        return False