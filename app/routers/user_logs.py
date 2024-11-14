from fastapi import APIRouter
from ..database import SessionDep
from ..utils import get_user_activity
from ..auth import get_current_user

router = APIRouter()

@router.get('/activity')
def get_user_activity():
    pass