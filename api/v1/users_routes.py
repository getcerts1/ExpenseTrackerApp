from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.userschema import CreateUser, RespondUser
from crud.user_crud import create_user_crud




router = APIRouter()


@router.post("/user", response_model= RespondUser)
async def create_user(schema:CreateUser, db: Session = Depends(get_db)):
    schema_dict = schema.model_dump()
    user = create_user_crud(schema_dict, db)
    return user


