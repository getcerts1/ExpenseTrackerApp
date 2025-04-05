from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db.database import get_db
from crud.expenses_crud import create_expense_crud, get_list_categories, get_expense_by_id_crud
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


@router.get("/categories/{category}")
async def list_by_category(category: str, db: Session = Depends(get_db),
                           user: dict = Depends(verify_token)
                           ):

    user_id = user.id
    if category == "Food&Dining":
        category = "Food & Dining"
    output = get_list_categories(category, user_id,db)

    return output


@router.get("/expense/{id}", response_model=ReturnExpense)
async def get_expense_by_id(id: int, db: Session = Depends(get_db),
                            user: dict = Depends(verify_token)):

    user_id = user.id
    expense = get_expense_by_id_crud(id,user_id, db)

    return expense