from pydantic import BaseModel
from datetime import date,datetime
from typing import Optional

class CreateSubscriptions(BaseModel):
    name:str
    category:str
    amount:float
    billing_cycle:str

    class Config:
        from_attributes=True

class ResponseModel(BaseModel):
    id:int    
    name:str
    category:str
    amount:float
    billing_cycle:str
    created_at:datetime
    start_date:date
    end_date:date
    status:str
    reminder:int
    updated_at:datetime
    class Config:
        from_attributes=True

class UpdateSubscription(BaseModel):
    name:Optional[str]=None
    category:Optional[str]=None
    amount:Optional[float]=None
    billing_cycle:Optional[str]=None
    start_date:Optional[date]=None
    status:Optional[str]=None
    reminder:Optional[int]=None
    class Config:
        from_attributes=True

class SignUp(BaseModel):
    email:str
    password:str
    class Config:
        from_attributes=True

class GetUser(BaseModel):
    id:int
    email:str
    created_at:datetime
    class Config:
        from_attributes=True

class login(BaseModel):
    email:str
    password:str
    class Config:
        from_attributes=True  

class UpdateUser(BaseModel):
    email:Optional[str]=None
    password:Optional[str]=None
    class Config:
        from_attributes=True

class Tokendata(BaseModel):
    id:int
    class Congif:
        from_attributes=True


class Token(BaseModel):
    access_token:str  
    token_type:str  
    class Congif:
        from_attributes=True                    