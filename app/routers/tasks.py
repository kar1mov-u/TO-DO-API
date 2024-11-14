from fastapi import HTTPException,APIRouter,Query,Depends
from datetime import datetime,date
from ..database import SessionDep
from ..auth import get_current_user
from ..utils import get_current_user_object,validate_user_to_task
from ..models.sql_models import TasksBase,TasksUpdate,TasksDB
from sqlmodel import select,desc,or_

router = APIRouter(tags=["Tasks"])

@router.post("/tasks/create")
def create_task(task:TasksBase,session:SessionDep, user:str=Depends(get_current_user)):
    user_db = get_current_user_object(session,user)
    task_db =TasksDB(**task.model_dump())
    task_db.user = user_db
    session.add(task_db)
    session.commit()
    session.refresh(task_db)    
    return task_db

@router.get('/tasks/{id}')
def get_task(id:int, session:SessionDep,user:str=Depends(get_current_user)):
    user_db = get_current_user_object(session,user)
    task = session.get(TasksDB,id)
    if not task:
        raise HTTPException(status_code=404, detail="The task is not avaiable")    
    if task.user_id!=user_db.id:
        raise HTTPException(status_code=404, detail="THis task does not belong to you")
    return task


# @router.get('/tasks/{date}')
# def get_by_date(date: date, session: SessionDep):
#     # Here, query the database to filter tasks by the specified date
#     start_of_day = datetime.combine(date, datetime.min.time())
#     end_of_day = datetime.combine(date, datetime.max.time())
#     tasks = session.exec(select(TasksDB).where(
#         TasksDB.created_at>=start_of_day,
#         TasksDB.created_at<= end_of_day
#         )).all()
#     return tasks

@router.get('/tasks')
def get_tasks(session:SessionDep,
              user:str=Depends(get_current_user),
              priority:bool=Query(default=False), 
              completed:bool=Query(default=None),
              keyword:str=Query(default=None),
              date: date=Query(default=None),
              offset:int=Query(default=0),
              limit:int=Query(default=100)):
    
    user_db = get_current_user_object(session,user)
    query = select(TasksDB)
    query = query.where(TasksDB.user_id==user_db.id)
    
    if date:
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        query = query.where(TasksDB.created_at>=start_of_day,TasksDB.created_at<=end_of_day)
    
    if completed is not None:
        query = query.where(TasksDB.completed ==completed)
    if priority:
        query = query.order_by(desc(TasksDB.priority))
    if keyword:
        query = query.where(or_(TasksDB.description.like(f"%{keyword}%"),TasksDB.title.like(f"%{keyword}%")))
    query = query.offset(offset).limit(limit)
    tasks = session.exec(query).all()
    return tasks
    

@router.patch("/tasks/{id}")
def update_task(id:int, u_task:TasksUpdate,session:SessionDep,user:str=Depends(get_current_user)):
    user_db = get_current_user_object(session,user)


    task_db = session.get(TasksDB,id)    
    if not task_db:
        raise HTTPException(status_code=404, detail="There is no such post")
    validate_user_to_task(user_db.id, task_db.user_id)
        
    task_data = u_task.model_dump(exclude_unset=True)
    for key,value in task_data.items():
        setattr(task_db,key,value)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@router.delete('/tasks/{id}')

def delete_task(id:int,session:SessionDep,user:str=Depends(get_current_user)):
    user_db = get_current_user_object(session,user)

    task = session.get(TasksDB,id)
    if not task:
        raise HTTPException(status_code=404, detail="There is no such task")
    if task.user_id!=user_db.id:
        raise HTTPException(status_code=404, detail="THis task does not belong to you")
    session.delete(task)
    session.commit()
    return {"data":"Task is deleted"}