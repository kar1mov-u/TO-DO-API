from fastapi import APIRouter,HTTPException
from ..models.sql_models import UserBase,UserDB,UserResponse
from ..database import SessionDep
from ..utils import hashing_pass
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
router = APIRouter()

@router.post('/users/create',response_model=UserResponse)
def craete_user(user:UserBase,session:SessionDep):
    try:
        user.password = hashing_pass(user.password)
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400,detail="Email or username is already in use")
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Unexpected Error occured")
    
@router.get('/users',response_model=list[UserResponse])
def get_users(session:SessionDep):
    users=session.exec(select(UserDB)).all()
    return users