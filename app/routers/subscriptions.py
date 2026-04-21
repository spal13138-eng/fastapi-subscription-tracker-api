from fastapi import FastAPI,HTTPException,status,Depends,APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from app import models,schemas
from datetime import datetime,date,timedelta
from app import oauth2

router=APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseModel)
def postSubscription(subscription:schemas.CreateSubscriptions,db:Session=Depends(get_db),
    current_user:models.User=Depends(oauth2.get_current_user)):

    start_date=datetime.utcnow().date()

    if subscription.billing_cycle=="monthly":
        end_date=start_date + timedelta(days=30)
    elif subscription.billing_cycle=="yearly":
        end_date=start_date + timedelta(days=365)  
    elif subscription.billing_cycle=="quaterly":
        end_date=start_date + timedelta(days=90)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="invalid billing cycle")          
    
    new_subscription=models.Subscription(
        name=subscription.name,
        category=subscription.category,
        amount=subscription.amount,
        billing_cycle=subscription.billing_cycle,
        start_date=start_date,
        end_date=end_date,
        owner_id=current_user.id
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


@router.get("/",response_model=list[schemas.ResponseModel])
def getSubscriptions(status:str=None,limit:int=10,offset:int=0,db:Session=Depends(get_db),
     current_user:models.User=Depends(oauth2.get_current_user)):
    
    subscription=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id)

    if status:
      subscription=subscription.filter(models.Subscription.status==status)\
      .order_by(models.Subscription.created_at)\
      .limit(limit)\
      .offset(offset)\
      .all()
 
    
    return subscription

# reminder for upcoming renewals

@router.get("/upcoming-renewals",response_model=list[schemas.ResponseModel])
def getReminder(db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    today=datetime.utcnow().date()

    subscription=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id,
    models.Subscription.status=="active").order_by(models.Subscription.created_at.asc()).all()

    upcoming=[]

    for subs in subscription:
        reminder_date=subs.end_date-timedelta(days=subs.reminder)

        if today>=reminder_date:
            upcoming.append(subs)


    return upcoming

# get subscriptions by name

@router.get("/{name}",response_model=schemas.ResponseModel)
def getSubscriptionbyName(name:str,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    
    subscription=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id,models.Subscription.name==name).first()

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You do not have any subscription of {name}")
    
    return subscription


# category wise subscription search

@router.get("/category/{category}",response_model=list[schemas.ResponseModel])
def getSubscriptionbyCategory(category:str,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    subscription=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id,models.Subscription.category==category).all()

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"you do not have any active subcription for this {category}")
    
    return subscription
 

@router.put("/{id}",response_model=schemas.ResponseModel)
def updateSubscription(id:int,updatesubcription:schemas.UpdateSubscription,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    subscription_query=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id,models.Subscription.id==id)
    subscription=subscription_query.first()

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Subscription with {id} is not found")
    
    update_data=updatesubcription.dict(exclude_unset=True)

    if "start_date" in update_data or "billing_cycle" in update_data:
      start_date=update_data.get("start_date",subscription.start_date)
      billing_cycle=update_data.get("billing_cycle",subscription.billing_cycle)

      if billing_cycle=="monthly":
          end_date=start_date+timedelta(days=30)
      elif billing_cycle=="quaterly":
          end_date=start_date+timedelta(days=90)
      elif billing_cycle=="yearly":
          end_date=start_date+timedelta(days=365)
      else:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid billing_cycle")
      
      update_data["end_date"]=end_date 

    subscription_query.update(update_data,synchronize_session=False) 



    db.commit()
    db.refresh(subscription)
    
    return subscription


@router.delete("/{id}")
def deleteSubcriptions(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):

    subscription=db.query(models.Subscription).filter(models.Subscription.owner_id==current_user.id,models.Subscription.id==id)

    if subscription.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Subscription is not found")
    
    subscription.delete(synchronize_session=False)

    db.commit()

    return{"message":"Subscription Successfully deleted"}