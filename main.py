import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.services.auth.authenticate import router as auth_router
from app.services.users.routers import router as user_router
from app.core.database import Base, engine  # Your models

# Fetch DB credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

app.include_router(router=auth_router, prefix="/rentals", tags=["rentals"])
app.include_router(router=user_router, prefix="/rentals", tags=["rentals"])

# For Server Health Check
@app.get("/")
def ping():
    return "You are good to go..."

