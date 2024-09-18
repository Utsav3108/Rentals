from pydantic import BaseModel
from typing import Optional
import uuid

# Login Body
class LoginBodyModel(BaseModel):
    email : str
    password : str

# Models
class Token(BaseModel):
    access_token: str
    token_type: str
    uid : uuid.UUID


class TokenData(BaseModel):
    user_email: Optional[str] = None


class UserMain(BaseModel):
    uid: uuid.UUID
    firstname: str
    lastname:  str
    email:  str 
    phone:  int 
    address: str

    class Config:
        from_attributes = True


class UserInDB(UserMain):
    hashed_password: str
