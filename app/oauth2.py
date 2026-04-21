from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError,jwt
from app import schemas,models
from app.config import settings

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

oauth_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encode=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode

def verify_access_token(token:str,credentials_Exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print(payload)

        id:int=payload.get("user_id")  

        if id is None:
            raise credentials_Exception

        token_data=schemas.Tokendata(id=id)  
    except JWTError as e:
        raise credentials_Exception

    return token_data


def get_current_user(token:str=Depends(oauth_scheme),db:Session=Depends(get_db)):

    credentials_Exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate":"bearer"}
    )
    
    token_data=verify_access_token(token,credentials_Exception)

    user=db.query(models.User).filter(models.User.id==token_data.id).first()

    if user is None:
        raise credentials_Exception
    
    return user

