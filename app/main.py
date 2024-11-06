from fastapi import FastAPI,HTTPException,Query
from sqlmodel import select,desc,or_
from datetime import date,datetime
from .database import create_db_and_tables,SessionDep
from .models.sql_models import TasksBase,TasksUpdate
app = FastAPI()




@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"data":"working"}


@app.post("/create")
def create_task(task:TasksBase,session:SessionDep):
    session.add(task)
    session.commit()
    session.refresh(task)    
    return task

@app.get('/tasks/{id}')
def get_task(id:int, session:SessionDep):
    task = session.get(TasksBase,id)
    if not task:
        raise HTTPException(status_code=404, detail="The task is not avaiable")    
    return task


@app.get('/tasks/{date}')
def get_by_date(date: date, session: SessionDep):
    # Here, query the database to filter tasks by the specified date
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    tasks = session.exec(select(TasksBase).where(
        TasksBase.created_at>=start_of_day,
        TasksBase.created_at<= end_of_day
        )).all()
    return tasks

@app.get('/tasks')
def get_tasks(session:SessionDep,
              priority:bool=Query(default=False), 
              completed:bool=Query(default=None),
              keyword:str=Query(default=None),
              date: date=Query(default=None),
              offset:int=Query(default=0),
              limit:int=Query(default=100)):
    query = select(TasksBase)
    
    if date:
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        query = query.where(TasksBase.created_at>=start_of_day,TasksBase.created_at<=end_of_day)
    
    if completed is not None:
        query = query.where(TasksBase.completed ==completed)
    if priority:
        query = query.order_by(desc(TasksBase.priority))
    if keyword:
        query = query.where(or_(TasksBase.description.like(f"%{keyword}%"),TasksBase.title.like(f"%{keyword}%")))
    query = query.offset(offset).limit(limit)
    tasks = session.exec(query).all()
    return tasks
    

@app.patch("/tasks/{id}")
def update_task(id:int, u_task:TasksUpdate,session:SessionDep):
    task_db = session.get(TasksBase,id)    
    if not task_db:
        raise HTTPException(status_code=404, detail="There is no such post")
    task_data = u_task.model_dump(exclude_unset=True)
    for key,value in task_data.items():
        setattr(task_db,key,value)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db

@app.delete('/tasks/{id}')
def delete_task(id:int,session:SessionDep):
    task = session.get(TasksBase,id)
    if not task:
        raise HTTPException(status_code=404, detail="There is no such task")
    session.delete(task)
    session.commit()
    return {"data":"Task is deleted"}