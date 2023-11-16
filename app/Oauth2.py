from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas
from . import  databases, models
from .config import  settings
oath_schemas = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # id: str = payload.get("user_id")
        id: str = str(payload.get("user_id"))
        print(id, 'this is the id that is supposed to be raised')

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        print(token_data, 'this is the token data')
    except JWTError:
        raise credentials_exception
    print(token_data, 't')
    return token_data


def get_current_user(token: str = Depends(oath_schemas), db: Session = Depends(databases.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could non validate user",
                                          headers={"WW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == int(token.id)).first()

    return  user
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTkzNjY3OTR9.BVwlxC5vtH_btpA_6-fl2tVcqIoddxp-oszDGzCEYJQ