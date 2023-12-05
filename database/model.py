from sqlalchemy import Integer , Column , String , TIMESTAMP ,text ,Boolean
from database.dataConnect import base

class User(base):
    __tablename__ = 'users'

    id = Column(Integer , primary_key=True , index=True)
    username = Column(String , unique=True , nullable=False)
    email = Column(String , unique=True , nullable=False ,index=True)
    fullname = Column(String , nullable=False)
    hashPassword = Column(String , nullable=False)
    is_disable = Column(Boolean , default=True)
    create_at = Column(TIMESTAMP(timezone=True) , default= text("now()"))
    last_active = Column(TIMESTAMP(timezone=True) , default= text("now()"))
    otp = Column(String , unique=True , nullable= False)

