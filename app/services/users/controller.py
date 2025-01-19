from passlib.context import CryptContext
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError

from app.core.database import get_db
from .database import User
from .models import ChangePassword, ResponseMessage


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/rentals/login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hash=hashed_password)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : Session = Depends(get_db)):

    from app.core.config import SECRET_KEY, ALGORITHM
    from app.services.auth.models import TokenData
    from .crud import get_user_db

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("user_email")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(user_email=user_email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_db(
        email = user_email, db = db)
    if user is None:
        raise credentials_exception
    return user


def changePassword(data : ChangePassword, db : Session, current_user : User) -> ResponseMessage:
    if data.new_password == data.confirm_password :
        try :
            new_hashed_password = get_password_hash(data.new_password)
            update_data = {"password": new_hashed_password}
            current_user.update(update_data=update_data)
            db.commit()
            db.refresh(current_user)  # Refresh to get the latest data from the database

            return ResponseMessage(message="Password Changed Successfully")
        except DataError as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Validation Error")
    else :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Confirm Password does not match")