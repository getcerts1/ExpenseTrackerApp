from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.expenses import Expense
from collections import Counter

VALID_CATEGORIES = [
"Food & Dining",
"Transportation",
"Housing",
"Entertainment",
"Healthcare"]


def common_element(arr):
    counts = Counter(arr)
    most_common = counts.most_common(1)
    return most_common


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

def get_summary(user_id, db: Session):

    entries = db.query(Expense).filter(
        (Expense.user_id == user_id)
    ).all()

    total_amount = 0
    popular_category = []


    for entry in entries:
        if entry.amount is not None:
            total_amount+=entry.amount

        popular_category.append(entry.category)

    result = common_element(popular_category)
    result_name, result_num = result[0]


    return { f"total spent: ${total_amount}, popular_category: {result_name}, with {result_num} times "}
