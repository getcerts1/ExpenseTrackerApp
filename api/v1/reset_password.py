from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError

from models.users import User
from db.database import get_db
from core.config import SECRET,ALGORITHM, EXPIRATION_TIME
from core.email import send_reset_email
from core.security import hash_pass


router = APIRouter()


""" user requests a password by entering their username/email, user existence is checked and then
a reset token is generated for authentication and sent to user email"""

@router.post("/request_password_reset/{username}")
async def request_reset_password(username: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User.username == username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")



        reset_token = jwt.encode({
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.now() + timedelta(minutes=EXPIRATION_TIME)

        }, SECRET, ALGORITHM)


        send_reset_email(user.username, reset_token)

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}"
        )



"""user clicks on the link and is provided a form where they enter a new password, this then triggers the 
below endpoint with the token and the password from the form, integrity and user existence is checked"""

@router.post("/reset-password/")
def reset_password(token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")

        if not user_id or not username:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Hash the new password and update it
        user.password = hash_pass(new_password)
        db.commit()
        db.refresh(user)

        return {"message": "Password updated successfully"}


    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}"

        )

