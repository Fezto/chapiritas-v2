from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app.config import DATABASE_URL
from app import models

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def lifespan(app: FastAPI):
    print("Creating database tables...")
    yield
