from passlib.context import  CryptContext
from jose import JWTError , jwt
from fastapi import HTTPException , Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Union , Annotated
from random import randint
from dotenv import load_dotenv
from datetime import datetime , timedelta
from email.message import EmailMessage
import smtplib 
import os

# from database.crud import get_user
from database.schemas import userInDB , User
from sqlalchemy.orm import Session

load_dotenv()

key = os.urandom(32)
SECRET_KEY = key.hex()
oauth2_schemes = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHEM = "HS256"
pwd_context = CryptContext(schemes=['bcrypt'] , deprecated = "auto")

def generate_hash_password(plain_password):
    return pwd_context.hash(plain_password)


def generate_OTP():
    return randint(100000 , 999999)


def send_otp_email(to_email, otp):
    email_user = os.getenv("email_user")
    email_password = os.getenv("email_password")

    subject = "Your OTP"
    body = f"Your Verification OTP is : {otp}"

    try:
        # Create an EmailMessage object
        message = EmailMessage()
        message.set_content(body)
        message["Subject"] = subject
        message["From"] = email_user
        message["To"] = to_email

        # Establish the SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_user, email_password)

            # Send the email message
            server.send_message(message)

        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print(f"Error sending email: {str(e)}")


def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)

def get_user(db , username : str):
    if username in db :
        user_dict = db[username]
        return userInDB(**user_dict)
    
def authenticate_user(db , username , password ):
    userData = get_user(db = db , username=username)

    if not userData :
        return False
    if not verify_password(password , userData.hashed_password) :
        return False
    
    return userData

def create_access_token(data : dict , expire_delta : Union[timedelta , None ] = None):
    if expire_delta :
        expire = datetime.utcnow() + expire_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp" : expire})
    jwt_encode = jwt.encode(data , SECRET_KEY , algorithm=ALGORITHEM )

    return jwt_encode



def get_current_user(db , token : Annotated[str , Depends(oauth2_schemes)] ):
    credentials_exception  = HTTPException(
        status_code=401,
        detail="could not valid crediantial",
        headers={"www-authenticate" : "Bearer"}
    )

    try :
        payload = jwt.decode(token , SECRET_KEY , algorithms=ALGORITHEM )
        username = payload.get("sub")

        if username is None :
            raise credentials_exception

    except :
        raise credentials_exception
    
    user = get_user(db = db , username=username)

    if user is None :
        raise credentials_exception
    
    return user


def get_current_active_user(current_user : Annotated[User , Depends(get_current_user)]):
    if current_user.disabled :
        raise HTTPException(status_code=400,detail='Disabled account')
    return current_user
    
def get_user(db : Session , username: int):
    return db.query(User).filter(User.username == username).first()