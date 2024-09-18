from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Depends, HTTPException, status
from .models import RegisterModel, RegisterResponse, UpdateModel, ChangePassword, ForgotPasswordModel, ResponseMessage
from .utills import get_current_user
from .database import User
from sqlalchemy.exc import DataError
from .utills import get_password_hash, verify_password

router = APIRouter()

# ==================  ERRORs ===================================

REGISTRATION_ERROR = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Exist")
USER_NOT_FOUND_ERROR = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
PASSWORD_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Password or Confirm Password are not Same.")

# ==================  User Register Endpoint ===================================
@router.post("/user/register")
def register_user(data : RegisterModel, db : Session = Depends(get_db)):

    from .crud import get_user_db, create_user
    from .database import User
    from .utills import get_password_hash
    import uuid

    if data.password != data.confirm_password :
        raise PASSWORD_ERROR

    user = get_user_db(email=data.email, db=db)

    if user is not None:
        raise REGISTRATION_ERROR
    else :
        hashed = get_password_hash(data.password)
        uid = uuid.uuid4()
        user =  User(
            uid = uid,
            firstname = data.firstname,
            lastname = data.lastname,
            email = data.email,
            phone = data.phone,
            address = data.address,
            password = hashed
            )
        create_user(db=db, user=user)
        return RegisterResponse(message="User Created Successfully")
    

# ==================  User Details Endpoint ===================================    
@router.get("/user/{email}")
def get_user(email: str, db : Session = Depends(get_db)):
    from .crud import get_user_db

    user = get_user_db(email = email, db = db)

    if user is None : 
        raise USER_NOT_FOUND_ERROR
    else :
        return user

# ==================  User Change Password Endpoint ===================================   
from fastapi.security import OAuth2PasswordBearer

oauh2scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)
@router.patch("/user")
def change_user_field(data : UpdateModel, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)): 

    

    update_data = data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No fields to update")
    try:
        # Use the SQLAlchemy model's update method to dynamically update the fields
        current_user.update(update_data)
        
        # Commit the changes to the database
        db.commit()
        db.refresh(current_user)  # Refresh to get the latest data from the database

        return {"message": "Update Successfully"}
    except DataError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Validation Error")


# ==================  User Delete Endpoint ===================================  
@router.delete("/user/{email}")
def delete_user_field(email : str, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.email == email).first()

    # If user not found, raise a 404 error
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Optional: Check if current_user is authorized to delete (e.g., is admin or deleting themselves)
    if current_user.uid != user.uid:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    # Delete the user
    db.delete(user)
    db.commit()

    # Return no content (204)
    return

#  ==================  User Change Password Endpoint ===================================

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
        raise PASSWORD_ERROR

@router.patch("/user/changePassword")
def user_password_change(data : ChangePassword, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    

    user = db.query(User).filter(User.email == current_user.email).first()
    print("user: ", user.email, user.password, get_password_hash(data.old_password))

    isOldPwdCorrect = verify_password(data.old_password, user.password)

    if not isOldPwdCorrect :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old Password is incorrect")
    
    return changePassword(data = data, db = db, current_user = current_user)
    
#  ==================  User Forget Password Endpoint ===================================    
@router.patch("/user/forgotpassword")
def user_password_forgot(data : ForgotPasswordModel, db : Session = Depends(get_db),  current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.email == "v@p.com").first()
    print("user", not user)

    if not user:
        raise USER_NOT_FOUND_ERROR
    return changePassword(data = data, db = db, current_user = user)