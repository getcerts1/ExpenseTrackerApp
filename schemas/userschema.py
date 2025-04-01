from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class CreateUser(BaseModel):
    username: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value