from pydantic import BaseModel
import uuid
from typing import Optional

class RegisterResponse(BaseModel):
    message : str = "User Created Successfully"

class RegisterModel(BaseModel):
    
    # uid will be formed on the fly.
    firstname : str
    lastname : str
    phone : int
    address : str
    email : str
    password : str
    confirm_password : str

class UpdateModel(BaseModel):
    firstname : Optional[str]
    lastname : Optional[str]
    phone : Optional[str]
    address : Optional[str]


class ForgotPasswordModel(BaseModel):
    new_password : str
    confirm_password : str

class ChangePassword(ForgotPasswordModel):
    old_password : str

class ResponseMessage(BaseModel):
    message : str