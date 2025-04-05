from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.expenses import Expense

VALID_CATEGORIES = [
"Food & Dining",
"Transportation",
"Housing",
"Entertainment",
"Healthcare"]


def create_expense_crud(schema, user_id: int, db: Session):
    expense = Expense(**schema, user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_list_categories(category: str, user_id: int, db: Session):
    if category not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid category")

    category_expenses = db.query(Expense).filter(
        (Expense.user_id == user_id) & (Expense.category == category)
    ).all()

    if not category_expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No expenses found for category '{category}'"
        )

    return category_expenses


def get_expense_by_id_crud(id: int,user_id, db: Session):
    expense = db.query(Expense).filter(
        (Expense.id == id) & (Expense.user_id == user_id)
    ).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expense not found")

    return expense