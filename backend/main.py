import os
from urllib.parse import quote
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg://app:app@db:5432/tasks')

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "tasks")
    db_user = os.environ.get("DB_USER", "app")
    db_password = os.environ.get("DB_PASSWORD", "app")

    DATABASE_URL = (
        f"postgresql+psycopg://{quote(db_user, safe='')}:"
        f"{quote(db_password, safe='')}@{db_host}:{db_port}/{db_name}"
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL)'))
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[os.environ.get('FRONTEND_ORIGIN','http://localhost:3000')], allow_methods=['GET','POST'], allow_headers=['Content-Type'])

@app.get('/health')
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return {'status': 'ok'}
    except SQLAlchemyError:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail='Database unavailable')

@app.get('/api/tasks')
def list_tasks():
    with engine.connect() as conn:
        rows = conn.execute(text('SELECT id, title FROM tasks ORDER BY id DESC')).mappings().all()
    return [dict(row) for row in rows]

from pydantic import BaseModel, Field
class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)

@app.post('/api/tasks', status_code=201)
def add_task(task: TaskIn):
    with engine.begin() as conn:
        row = conn.execute(text('INSERT INTO tasks(title) VALUES (:title) RETURNING id, title'), {'title': task.title}).mappings().one()
    return dict(row)
