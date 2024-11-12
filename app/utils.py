from passlib.context import CryptContext
from .database import SessionDep
from sqlmodel import select
from .models.sql_models import UserDB
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