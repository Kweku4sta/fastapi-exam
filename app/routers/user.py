from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from .. import schemas, utils, models
from ..databases import get_db

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
def crate_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
