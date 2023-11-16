from datetime import timedelta
from typing import Annotated

from fastapi import status, Response, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import databases, schemas, models, utils, Oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post("/login",response_model=schemas.Token)
def login(user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(databases.get_db)):
    user = db.query(models.User).filter(models.User.email == user_details.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")

    if not utils.verify_password(user_details.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")

    access_token = Oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token")
def login_for_access_token(userCredentials: schemas.UserLogin, db: Session = Depends(databases.get_db)):
    user = db.query(models.User).filter(models.User.email == userCredentials.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username, "scopes": form_data.scopes},
    #     expires_delta=access_token_expires,
    # )
    return {"access_token": 'token', "token_type": "bearer"}


@router.get('/hello')
def get_hello():
    return {"Hello": "Hello"}
