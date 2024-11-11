from fastapi import HTTPException,APIRouter,Query
from datetime import datetime,date
from ..database import SessionDep
from ..models.sql_models import TasksBase,TasksUpdate,TasksDB
from sqlmodel import select,desc,or_

router = APIRouter()

@router.post("/tasks/create")
def create_task(task:TasksBase,session:SessionDep):
    task_db =TasksDB(**task.model_dump())
    session.add(task_db)
    session.commit()
    session.refresh(task_db)    
    return task_db

@router.get('/tasks/{id}')
def get_task(id:int, session:SessionDep):
    
    task = session.get(TasksDB,id)
    if not task:
        raise HTTPException(status_code=404, detail="The task is not avaiable")    
    return task


@router.get('/tasks/{date}')
def get_by_date(date: date, session: SessionDep):
    # Here, query the database to filter tasks by the specified date
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    tasks = session.exec(select(TasksDB).where(
        TasksDB.created_at>=start_of_day,
        TasksDB.created_at<= end_of_day
        )).all()
    return tasks

@router.get('/tasks')
def get_tasks(session:SessionDep,
              priority:bool=Query(default=False), 
              completed:bool=Query(default=None),
              keyword:str=Query(default=None),
              date: date=Query(default=None),
              offset:int=Query(default=0),
              limit:int=Query(default=100)):
    query = select(TasksDB)
    
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
def update_task(id:int, u_task:TasksUpdate,session:SessionDep):
    task_db = session.get(TasksDB,id)    
    if not task_db:
        raise HTTPException(status_code=404, detail="There is no such post")
    task_data = u_task.model_dump(exclude_unset=True)
    for key,value in task_data.items():
        setattr(task_db,key,value)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@router.delete('/tasks/{id}')
def delete_task(id:int,session:SessionDep):
    task = session.get(TasksDB,id)
    if not task:
        raise HTTPException(status_code=404, detail="There is no such task")
    session.delete(task)
    session.commit()
    return {"data":"Task is deleted"}