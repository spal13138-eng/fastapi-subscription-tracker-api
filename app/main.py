from fastapi import FastAPI
from app import models
from app.database import Base,engine
from app.routers import subscriptions
from app.routers import auth,user
models.Base.metadata.create_all(bind=engine)


app=FastAPI()

@app.get("/")
def testing():
    return {"message":"API is running"}


app.include_router(subscriptions.router)
app.include_router(user.router)
app.include_router(auth.router)