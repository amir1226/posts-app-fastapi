from typing import Optional
from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2
from ..schemas import PostCreate, PostResponse

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # PSYCOPG2 implementation of get_posts
    """cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall() """
    
    ## contains is case sensitive == "like" in postgres, I changed to "ilike"
    posts = db.query(models.Post).filter(models.Post.title.ilike(f'%{search}%')).limit(limit).offset(skip).all() 
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), 
                      current_user = Depends(oauth2.get_current_user)):
    # PSYCOPG2 implementation of create_post
    """cursor.execute('''INSERT INTO posts (title, content, published) 
                   VALUES (%s,%s,%s) RETURNING * ''', (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit() """
    # new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=PostResponse) #response_model_include/exclude= {} or []
async def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # PSYCOPG2 implementation of get_post
    """cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone() """
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} was not found"} """  
    return post


@router.put("/{id}", response_model=PostResponse)
async def update_post(id:int, post: PostCreate, db: Session = Depends(get_db), 
                      current_user = Depends(oauth2.get_current_user)):
    # PSYCOPG2 implementation of update_post
    """     cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s
                    RETURNING *''',
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone() """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_searched = post_query.first()
    
    if post_searched is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        
    if post_searched.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}")
async def delete_post(id:int, db: Session = Depends(get_db),
                      current_user = Depends(oauth2.get_current_user)):
    # PSYCOPG2 implementation of delete_post
    """ cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone() """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_searched = post_query.first()

    if post_searched is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    
    if post_searched.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)