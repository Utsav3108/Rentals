from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .models import LoginBodyModel, UserInDB, Token

from fastapi import APIRouter

from app.services.users.crud import get_user_db
from app.core.database import get_db
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from sqlalchemy.orm import Session

# to get a string like this run:
# openssl rand -hex 32
router  = APIRouter()

# Make Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Init OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
# Authenticate the User
def authenticate_user(db : Session, email: str, password: str):
    user = get_user_db(email=email, db=db)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user

# Create the Access Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login_for_access_token(login_data: LoginBodyModel,  db : Session = Depends(get_db)) -> Token:

    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = float(ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_expires = timedelta(minutes=access_token)
    access_token = create_access_token(
        data={"user_email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", uid=user.uid)

