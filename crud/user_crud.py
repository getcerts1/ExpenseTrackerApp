from fastapi import HTTPException, status, responses
from sqlalchemy.orm import Session
from models.users import User
from core.security import hashed_pass



"""--- POST ENDPOINT ---"""


def create_user_crud(schema, db: Session):
    user = db.query(User).filter(User.username == schema["username"]).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user exists")

    new_pass = hashed_pass(schema.get("password"))
    schema["password"] = new_pass

    new_user = User(**schema)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


""" --- DELETE ENDPOINT --- """

