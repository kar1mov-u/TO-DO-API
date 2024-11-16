from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import tasks,users,user_logs
app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(user_logs.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"data":"working"}
