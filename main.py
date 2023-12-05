from fastapi import FastAPI , Depends , HTTPException , status
from sqlalchemy.orm import Session
from datetime import datetime , timedelta , timezone

from database.dataConnect import SessionLocal , engin
from database.model import base
from database.schemas import UserCreate
from database.crud import create_user , get_user_by_email
from app.schemas import OTP 
from app.services import generate_OTP , send_otp_email

base.metadata.create_all(bind = engin)

appOTP = FastAPI()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@appOTP.post("/create/user/")
def register_user(user : UserCreate , db : Session = Depends(get_db)):
    db_user = get_user_by_email(db , user.email)
    if db_user :
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # global otpCode
    global otpStoreTime

    otpCode = generate_OTP()
    send_otp_email(user.email ,otpCode)
    otpStoreTime = datetime.utcnow()

    create_user(db , user , otpCode)
    

    # remain to store data in database
    return user
    
@appOTP.post("/verify/otp/")
# def verification_otp(otp : OTP ,db : Session = Depends(get_db) , user : dict = Depends(register_user)):
def verification_otp(otp : str , email : str , db : Session = Depends(get_db)):
    
    user = get_user_by_email(db , email)

    current_utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    if current_utc_time > user.create_at + timedelta(minutes=10) :
        raise HTTPException(status_code= status.HTTP_410_GONE , detail="OTP is Expired")

    if otp != user.otp :
        raise HTTPException(status_code=401 , detail="OTP Not Verifyed")
    
    return "OTP Verify Successfuly"


@appOTP.post("/user/me/")
def login_user():
    pass
