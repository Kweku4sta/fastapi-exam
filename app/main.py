from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi import Response
from starlette.middleware.cors import CORSMiddleware

from . import models, schemas, utils
from .databases import engine, get_db
from .routers import post, user,auth, votes
from .config import  settings

models.Base.metadata.create_all(bind=engine)
origins = ["https://www.google.com"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": 'hello welcome to the world of fast api'}
