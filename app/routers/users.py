from fastapi import APIRouter,HTTPException,Depends
from ..models.sql_models import UserBase,UserDB,UserResponse,UserLogin
from ..database import SessionDep
from datetime import datetime,timedelta
from ..utils import hashing_pass,authenticate_user,log_activity
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2AuthorizationCodeBearer,OAuth2PasswordRequestForm
from ..auth import ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token,Token,get_current_user
from sqlmodel import select
router = APIRouter(tags=["Users"])

@router.post('/users/create',response_model=UserResponse)
def craete_user(user:UserBase,session:SessionDep):
    try:
        user.password = hashing_pass(user.password)
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        log_activity(session,user_db.id,"User was created")
        return user_db
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400,detail="Email or username is already in use")
    except Exception as e :
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected Error occured  {e}")
    
@router.get('/users',response_model=list[UserResponse])
def get_users(session:SessionDep):
    users=session.exec(select(UserDB)).all()
    return users

@router.post('/users/login')
def loggin_user(session:SessionDep,user_data:OAuth2PasswordRequestForm=Depends()):
    user = authenticate_user(session,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate":"Bearer"})
    #craete JWT token 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token  = create_access_token(
        data = {"sub":user.email}, expires_delta=access_token_expires
    )
    log_activity(session,user.id,"User logged in")
    return Token(access_token=access_token,token_type="bearer")

@router.get('/users/me', response_model=UserResponse)
def get_user(session:SessionDep,user:str=Depends(get_current_user)):
    user_db = session.exec(select(UserDB).where(UserDB.email==user)).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="This is user is not found")
    return user_db