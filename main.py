from http.client import HTTPResponse
from fastapi import FastAPI
from app.services.auth.authenticate import router as auth_router
from app.services.users.routers import router as user_router

import uvicorn
app = FastAPI()

app.include_router(router=auth_router, prefix="/rentals", tags=["rentals"])
app.include_router(router=user_router, prefix="/rentals", tags=["rentals"])


# For Server Health Check
@app.get("/")
def ping():
    return "You are good to go..."

