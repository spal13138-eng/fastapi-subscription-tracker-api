from sqlalchemy import Column,Integer,BOOLEAN,String,Float,Date,DateTime,ForeignKey
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import Relationship


class Subscription(Base):
    __tablename__="subscriptions"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    category=Column(String,nullable=False)
    amount=Column(Float,nullable=False)
    billing_cycle=Column(String,nullable=False)

    start_date=Column(Date,nullable=False)
    end_date=Column(Date,nullable=False)

    status=Column(String,default="active")
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    reminder=Column(Integer,default=4)
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    owner=Relationship("User")

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,nullable=False)    
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
