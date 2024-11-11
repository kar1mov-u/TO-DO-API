from fastapi import APIRouter
from ..models.sql_models import UserBase
router = APIRouter()

@router.post('/users/create')
def craete_user(user:UserBase):
    pass