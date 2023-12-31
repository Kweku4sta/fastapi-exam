from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from  .. import  databases, models, schemas, Oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(databases.get_db), current_user: int = Depends(Oauth2.get_current_user) ):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    query_vote = db.query(models.Vote).filter(models.Post.id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = query_vote.first()

    if(vote.dir == 1):
        if found_vote:
            raise  HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already "
                                                                              f"voted on a post on {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": " voted successfully"}
    else:
        if not found_vote:
            raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        query_vote.delete(synchronize_session = False)
        db.commit()
        return  {"message": "successfully deleted vote"}
