
from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2
from ..schemas import Vote

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)) :
    
    found_post = db.query(models.Post).filter_by(id=vote.post_id).first()
    
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f'Post with id {vote.post_id} does not exist.')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                        models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"succesfully deleted vote"}
