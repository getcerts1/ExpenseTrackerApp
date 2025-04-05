from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from core.security import verify_token
from db.database import get_db
from schemas.userschema import CreateUser, RespondUser, PatchUser
import crud.user_crud




router = APIRouter(
    tags=["Users"]
)


@router.get("/getuser/{username}", response_model=RespondUser)
async def get_user(username: str, db: Session = Depends(get_db),
                   user: dict = Depends(verify_token)):
    user = crud.user_crud.get_user_crud(username, db)
    return user


@router.post("/user", response_model= RespondUser)
async def create_user(schema:CreateUser, db: Session = Depends(get_db)):
    schema_dict = schema.model_dump()
    user = crud.user_crud.create_user_crud(schema_dict, db)
    return user


@router.put("/edituser/{username}",response_model=RespondUser)
async def put_user(username: str, schema: CreateUser, db: Session = Depends(get_db),
                   user: dict = Depends(verify_token)):
    schema_dict = schema.model_dump()
    user = crud.user_crud.put_user_crud(username,schema_dict, db)
    return user

@router.patch("/patchuser/{username}", response_model=RespondUser)
async def patch_user(username: str, schema: PatchUser, db: Session = Depends(get_db),
                     user: dict = Depends(verify_token)):
    schema_dict = schema.model_dump()
    user = crud.user_crud.patch_user(username, schema_dict, db)
    return user

@router.delete("/deleteuser/username")
async def delete_user(username: str, db: Session = Depends(get_db),
                      user: dict = Depends(verify_token)):
    user = crud.user_crud.delete_user_crud(username, db)
    return user