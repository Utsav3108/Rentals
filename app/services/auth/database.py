# from app.core.database import SessionLocal, get_db
# from .models import UserMain, UserInDB
# from app.services.users.database import User
# # from .authenticate import get_password_hash
# from uuid import uuid4
# from sqlalchemy.orm import Session
# from fastapi import Depends
# # Our Data
# uid = uuid4
# firstname = "Aditya"
# lastname = "Shinde"
# email = "a@s.com"
# phone = 7418529631
# address = "Nikol, Ahmedabad"
# password = "123321"

# userobj = User(
#                 uid = uid, 
#                firstname = firstname, 
#                lastname = lastname, 
#                phone = phone, 
#                email = email, 
#                address = address,
#                password = password
#                )

# # Create Method
# def create_user(db : Session, user: UserMain):
#     # fake_hashed_password = user.password + "notreallyhashed"
#     db_user = userobj
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # Get Method
# def get_user_db( email: str, db: Session = Depends(get_db)):
#     return db.query(User).filter(User.email == email).first()
