from fastapi.security import OAuth2PasswordBearer

from app.services.users.crud import get_user_db
from app.core.config import SECRET_KEY, ALGORITHM

import jwt

from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext

from .models import UserInDB
from sqlalchemy.orm import Session

# to get a string like this run:
# openssl rand -hex 32


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

