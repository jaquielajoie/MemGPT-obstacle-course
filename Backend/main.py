import os 
from fastapi import FastAPI, status, Depends, HTTPException
import Backend.models 
from Backend.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Annotated
from sqlalchemy.orm import Session
import re
from langserve import add_routes
import Backend.auth 
from Backend.auth import get_current_user
from pydantic import BaseModel 

from Backend.agent import agent_executor

app = FastAPI()
app.include_router(Backend.auth.router)

Backend.models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Backend.models.User, Depends(get_current_user)] 

# FIXME: This is a temporary solution to get the chatbot working
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the routes to the app
@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return {"User" : user}

class Prompt(BaseModel):
    text: str

@app.post("/chatbot")
def chatbot(user: user_dependency, prompt: Prompt):

    response = agent_executor.run(prompt.text)
    return {"message": response}

