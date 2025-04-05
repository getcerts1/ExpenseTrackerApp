from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Ensure project path is set
from db.database import Base,engine
from api.v1 import users_routes, login, reset_password, expenses_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/test")
async def test():
    return {"message":"returned successful"}



app.include_router(users_routes.router)
app.include_router(expenses_routes.router)
app.include_router(login.router)
app.include_router(reset_password.router)