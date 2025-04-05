from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import get_db
from models.users import User
from core.config import SECRET,ALGORITHM,EXPIRATION_TIME
from jose import JWTError, jwt

password_context = CryptContext(schemes="bcrypt")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def hash_pass(password: str):
    new_password = password_context.hash(password)
    return new_password


def verify_password(clear_text_password, hashed_password):
    is_equal = password_context.verify(clear_text_password, hashed_password)
    return is_equal


def create_token(payload: dict):
    payload_copy = payload.copy()
    now = datetime.now()
    expiration = now + timedelta(minutes=EXPIRATION_TIME)

    payload_copy.update({
        "exp": int(expiration.timestamp()),
        "iat": int(now.timestamp())
    })

    token = jwt.encode(payload_copy, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        username: str = payload.get("username")

        #check for existing payload attributes
        if not user_id or not username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed payload")

        #check for user from the database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


        #check if user db has not been modified
        if user_id != user.id or username != user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="payload doesn't match backend!")



        return user

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}"
        )


