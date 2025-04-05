from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db.database import get_db
from crud.expenses_crud import create_expense_crud
from schemas.expenseschema import CreateExpense, ReturnExpense
from core.security import verify_token




router = APIRouter()


@router.post("/new-expense", response_model=ReturnExpense)
async def create_expense(schema: CreateExpense, db: Session = Depends(get_db),
                             user: dict = Depends(verify_token)):

    print(user)
    schema_dict = schema.model_dump()
    user_id = user.id
    expense = create_expense_crud(schema_dict, user_id, db)
    return ReturnExpense.model_validate(expense)