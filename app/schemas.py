from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class CreateUserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode: True


class PostBase(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: Optional[bool] = True
    created_at: Optional[datetime] = None
    owner: CreateUserResponse


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    owner_id: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    # id: str | None = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)


class PostOut(BaseModel):
    Post: PostBase
    votes: int

    class Config:
        orm_mode = True
