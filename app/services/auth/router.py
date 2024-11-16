from .authenticate import authenticate_user, timedelta, create_access_token
from fastapi import APIRouter
from app.core.database import get_db
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from .models import LoginBodyModel, Token
from fastapi import Depends, HTTPException, status, Request, Query

from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy.orm import Session

from google.oauth2 import id_token
from google.auth.transport import requests

from pydantic import BaseModel

router  = APIRouter()

@router.post("/login")
async def login_for_access_token(login_data: LoginBodyModel,  db : Session = Depends(get_db)) -> Token:

    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = int(ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_expires = timedelta(minutes=access_token)
    access_token = create_access_token(  
        data={"user_email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", uid=user.uid)

from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI 



@router.get("/google")
def go_to_google_signin():
    #redirect_uri = request.url_for('auth_callback')
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id=118806692893-ss14d4cvtvrvmigqh275hsuf536irfed.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/rentals/api/auth/google-callback&response_type=code&scope=openid email profile"
    return RedirectResponse(url=google_auth_url)

class GoogleAuthResponse(BaseModel):
    access_token: str
    id_token: str
    user_info: dict

@router.get("/api/auth/google-callback", response_model=GoogleAuthResponse)
async def google_callback(code: str = Query(...)):
    try:
        # Token exchange
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data, headers=headers)

            if token_response.status_code != 200:
                raise HTTPException(status_code=token_response.status_code, detail="Token exchange failed")

            tokens = token_response.json()
            access_token = tokens.get("access_token")
            id_token = tokens.get("id_token")

        # User info retrieval
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
            if userinfo_response.status_code != 200:
                raise HTTPException(status_code=userinfo_response.status_code, detail="Failed to fetch user info")

            user_info = userinfo_response.json()

        return {"access_token": access_token, "id_token": id_token, "user_info": user_info}

    except Exception as e:
        # Log and re-raise the error with details for debugging
        print(f"Error in google_callback: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    