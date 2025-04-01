from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Ensure project path is set
from db.database import Base,engine
from models.users import User
from models.expenses import Expense

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/test")
async def test():
    return {"message":"returned successful"}