from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username : str
    email : str
    fullname : str

class UserCreate(UserBase):
    password : str

class User(UserBase):
    id : int
    is_active : bool = True
    create_at : datetime = datetime.utcnow()
    last_active : datetime = datetime.utcnow()

    class config :
        orm_model = True

class userInDB(User):
    password : str