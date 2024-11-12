import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
SECRET_KEY = "31bb6132fe4890d1740653c2bc25bfe6895bc355a1b9613a0609c8822519d6ab"
ALGHORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class Token(BaseModel):
    access_token: str
    token_type: str
    

def create_access_token(data:dict,expires_delta:timedelta | None=None):
    to_encode= data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+expires_delta
    else:
        expire  =datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGHORITHM)
    return encoded_jwt

def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGHORITHM])
        user_email = payload.get('sub')
        if not user_email:
            raise HTTPException(status_code=403, detail="Invalid Credentials")
        return user_email
    except InvalidTokenError:
        raise credentials_exception
        