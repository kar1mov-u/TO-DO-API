from passlib.context import CryptContext
pwd_context =  CryptContext(schemes=['bcrypt'], deprecated="auto")

def hashing_pass(plain_pass):
    return pwd_context.hash(plain_pass)

def check_pass(hashed_pass,plain_pass):
    return pwd_context.verify(plain_pass,hashed_pass)