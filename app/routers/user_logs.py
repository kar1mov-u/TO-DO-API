from fastapi import APIRouter,Depends
from ..database import SessionDep

from ..auth import get_current_user
from ..utils import get_current_user_object
from ..models.sql_models import ActivityDB
from sqlmodel import select

router = APIRouter()

@router.get('/activity')
def get_user_activity(sesion:SessionDep,user:str=Depends(get_current_user)):
    user_db = get_current_user_object(sesion,user)
    logs = sesion.exec(select(ActivityDB).where(ActivityDB.user_id==user_db.id)).all()
    return logs
    