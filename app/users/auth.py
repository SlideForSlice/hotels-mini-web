import os
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UsersDAO
from datetime import datetime, timedelta, timezone

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=algorithm
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        raise HTTPException(status_code=401)
    return user