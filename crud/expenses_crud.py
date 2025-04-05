from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.expenses import Expense




def create_expense_crud(schema, user_id: int, db: Session):
    expense = Expense(**schema, user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense