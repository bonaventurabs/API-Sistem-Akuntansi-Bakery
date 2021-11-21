from datetime import datetime, timedelta
from typing import Optional

import hashlib
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.schemas import Token, User, TokenData
from src.models import Pengguna
from .database import get_db

class UserHandler():
    SECRET_KEY = "7fb37f84964f9eabe3898d94b5a9a0fb3131ced462886a8ce43dab60ec02d58f"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def verify_password(plain_password, hashed_password):
        return UserHandler.get_password_hash(plain_password) == hashed_password

    def get_password_hash(password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password

    def get_user(db, username: str,):
        user = db.query(Pengguna).filter(Pengguna.username == username).first()
        if user is not None:
            user_dict = jsonable_encoder(user)
            return User(**user_dict)

    def authenticate_user(db, username: str, password: str):
        user = UserHandler.get_user(db, username)
        if not user:
            return False
        if not UserHandler.verify_password(password, user.password):
            return False
  
        return user

    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=45)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, UserHandler.SECRET_KEY, algorithm=UserHandler.ALGORITHM)
        return encoded_jwt

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, UserHandler.SECRET_KEY, algorithms=[UserHandler.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise credentials_exception
        user = UserHandler.get_user(db, username=token_data.username)
        if user is None:
            raise credentials_exception
            
        return User(**jsonable_encoder(user))