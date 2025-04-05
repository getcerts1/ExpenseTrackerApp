from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

class CreateExpense(BaseModel):
    category: str
    description: Optional[str] = None
    amount: float

    @field_validator("category")
    def validate_category(cls, value:str):
        valid_categories = ["Food & Dining", "Transportation", "Housing",
                            "Entertainment", "Healthcare"]

        if value not in valid_categories:
            raise ValueError("category type is wrong")

        return value

    class Config:
        from_attributes = True

class ReturnExpense(BaseModel):
    id: int
    user_id: int
    category: str
    description: Optional[str] = None
    amount: float
    time_created: datetime

    class Config:
        from_attributes = True


