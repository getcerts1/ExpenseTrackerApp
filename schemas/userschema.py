from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime




class CreateUser(BaseModel):
    username: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @field_validator("username")
    def validate_username(cls, value):
        domain_names = ["@gmail", "@yahoo", "@outlook"]
        for domain in domain_names:
            if domain in value:
                raise ValueError(f"username cannot contain {domain}")
            return value


class RespondUser(BaseModel):
    id:int
    username: str
    password: str
    time_created: datetime


class PatchUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @field_validator("username")
    def validate_username(cls, value):
        domain_names = ["@gmail", "@yahoo", "@outlook"]
        for domain in domain_names:
            if domain in value:
                raise ValueError(f"username cannot contain {domain}")
            return value