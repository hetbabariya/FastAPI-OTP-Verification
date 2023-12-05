from database.schemas import UserCreate
from database.model import User
from sqlalchemy.orm import Session
from app.services import generate_hash_password

def get_user_by_email(db : Session , email : str):
    return db.query(User).filter(User.email == email).first()

# def get_user(db : Session , username: int):
#     return db.query(User).filter(User.username == username).first()


def create_user(db : Session , user : UserCreate , otp : str):
    hashPassword = generate_hash_password(user.password)
    print("HASHED : ",hashPassword)
    db_user = User(username = user.username , email = user.email , fullname  = user.fullname, hashPassword = hashPassword , otp = otp)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def delete_user(db : Session,email : str):
#     user = get_user_by_email(db,email)
#     if not user:        
#         raise ValueError('Email does not exist')
#     else:
#         db.query()