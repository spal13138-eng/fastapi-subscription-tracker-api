from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import models,schemas,utils
from app.database import get_db
from app import oauth2

router=APIRouter(
    prefix="/signup",
    tags=["User"]
)

@router.post("/",response_model=schemas.GetUser,status_code=status.HTTP_201_CREATED)
def RegisterUser(user:schemas.SignUp,db:Session=Depends(get_db)):


    hashed_password=utils.hash(user.password)
    new_user=models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/",response_model=schemas.GetUser)
def getUser(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    user=db.query(models.User).filter(models.User.id==current_user.id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user is not found")
    
    return user

@router.put("/",response_model=schemas.GetUser)
def updateUser(updateUser:schemas.UpdateUser,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    user_query=db.query(models.User).filter(models.User.id==current_user.id)
    user=user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid request")
    
    user_query.update(updateUser.dict(exclude_unset=True),synchronize_session=False)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/")
def deleteUser(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    user=db.query(models.User).filter(models.User.id==current_user.id)

    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")

    user.delete(synchronize_session=False)
    db.commit()  

    return {"message":"User is successfully deleted"}  
    
    


    
    

