from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from fastapi.openapi.models import Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from .. import schemas, models, Oauth2
from ..databases import get_db

router = APIRouter()


@router.get("/sqlalchemy", response_model=List[schemas.PostOut])
def test_posts(db: Session = Depends(get_db),limit: int = 5, skip: int =0,search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results



@router.get("/ownerposts", response_model=List[schemas.PostBase])
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id ==current_user.id ).all()
    print(posts)
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(Oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email, "this is the user id")
    return new_post


@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_single_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this transaction")
    post_query.delete()
    db.commit()
    return Response(description="Post deleted successfully",status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def alter_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
#     post_query = db.query(models.PostCreate).filter(models.Post.id == id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     post_query.update(updated_post.dic(), synchronize_session = False)
#     db.commit()
#
#     return {"message": post_query.first()}

@router.put("/posts/{id}")
def alter_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        post_query.update(updated_post.dic(), synchronize_session=False)
        db.commit()
        return {"message": post_query.first()}
    except Exception as e:
        print(e)  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")
