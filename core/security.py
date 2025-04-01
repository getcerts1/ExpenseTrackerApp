from passlib.context import CryptContext

password_context = CryptContext(schemes="bcrypt")


def hashed_pass(password: str):
    new_password = password_context.hash(password)
    return new_password
