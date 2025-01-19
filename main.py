from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import sessionmaker
from app.services.auth.router import router as auth_router
from app.services.users.routers import router as user_routers
from app.services.sms.sms_otp import sms_router as sms_routers
from starlette.middleware.sessions import SessionMiddleware

from app.core.database import Base, engine  # Your models
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
# Fetch DB credentials from environment variables
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_USER = os.getenv("DB_USER", "user")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
# DB_NAME = os.getenv("DB_NAME", "mydatabase")

Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with allowed origins (e.g., specific frontend URLs)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router=auth_router, prefix="/rentals", tags=["Auth"])
app.include_router(router=user_routers, prefix="/rentals", tags=["User"])
app.include_router(router=sms_routers, prefix="/rentals", tags=["Sms"])
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# For Server Health Check
@app.get("/user_ping", tags=["Health Check"])
def ping():
    return "You are good to go..."

