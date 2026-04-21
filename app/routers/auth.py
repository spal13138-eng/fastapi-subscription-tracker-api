from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import models,schemas,utils
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from app import oauth2


router=APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/",status_code=status.HTTP_200_OK)
def loginUser(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}