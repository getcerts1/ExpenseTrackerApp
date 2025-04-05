from fastapi import HTTPException, status, responses
from sqlalchemy.orm import Session
from models.users import User
from core.security import hash_pass

"""--- GET ENDPOINT --- """

def get_user_crud(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    return user


"""--- POST ENDPOINT ---"""


def create_user_crud(schema, db: Session):
    user = db.query(User).filter(User.username == schema["username"]).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user exists")

    new_pass = hash_pass(schema.get("password"))
    schema["password"] = new_pass

    new_user = User(**schema)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


""" --- PUT ENDPOINT --- """

def put_user_crud(username, updated_schema, db: Session):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    new_pass = hash_pass(updated_schema["password"])
    updated_schema["password"] = new_pass

    for key, value in updated_schema.items():
        setattr(user, key, value)

    updated_user = User(**updated_schema)
    db.add(updated_user)
    db.commit()
    db.refresh(updated_user)

    return updated_user

""" --- PATCH ENDPOINT --- """

def patch_user(username, updated_schema, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    if "password" in updated_schema and updated_schema["password"]:
        updated_schema["password"] = hash_pass(updated_schema["password"])

    for key, value in updated_schema.items():
        if value is not None:
            setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

""" --- DELETE ENDPOINT --- """
def delete_user_crud(username, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    db.delete(user)
    db.commit()
    db.refresh(user)

    return {"message":f"successfully deleted user {username} with user id {user.id} "}
