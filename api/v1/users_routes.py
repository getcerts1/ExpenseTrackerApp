from fastapi import APIRouter
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.userschema import CreateUser
from crud.user_crud import create_user_crud




router = APIRouter()


@router.post("/user", response_model= CreateUser)
async def create_user(schema:CreateUser, db: Session = get_db):
    schema_dict = schema.model_dump()
    user = create_user_crud(schema_dict, db)
    return user


