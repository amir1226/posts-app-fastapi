from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
from sqlalchemy.orm import session
from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title : str = Field(title="Post title")
    content : str
    published : bool = True


# PSYCOPG2 connection
""" while True:
    try:
        # Come from .env file
        BASEDIR = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(BASEDIR, '.env'))    
        DB_USERNAME = os.getenv('DATABASE_USER') 
        DB_PASSWORD = os.getenv('DATABASE_PSW')

        conn = psycopg2.connect(host = 'localhost', dbname='fastapi', 
                                user=DB_USERNAME, password=DB_PASSWORD, port=5435, cursor_factory= RealDictCursor)
        
        cursor=conn.cursor()
        print('Database connection was succesfull!')
        break
        
    except Exception as error:
        print('Connecciont to database failed\nError: ', error)
        time.sleep(2) """
    
    

# posts = [{"id":1, "title":"First post", "content":"Contet test"},
#                      {"id":2, "title":"Second post", "content":"Pizza is the best!"}]

@app.get("/")
async def hello():
    return {"message": "Hello api"}



@app.get("/posts")
async def get_posts(db: session = Depends(get_db)):
    # PSYCOPG2 implementation of get_posts
    """cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall() """
    
    posts = db.query(models.Post).all()
    return{"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: session = Depends(get_db)):
    # PSYCOPG2 implementation of create_post
    """cursor.execute('''INSERT INTO posts (title, content, published) 
                   VALUES (%s,%s,%s) RETURNING * ''', (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit() """
    # new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get('/posts/{id}') 
async def get_post(id: int, db: session = Depends(get_db)):
    # PSYCOPG2 implementation of get_post
    """cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone() """
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} was not found"} """
    return {"data": post}


@app.put("/posts/{id}")
async def update_post(id:int, post: Post, db: session = Depends(get_db)):
    # PSYCOPG2 implementation of update_post
    """     cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s
                    RETURNING *''',
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone() """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return{"data": post_query.first()}


@app.delete("/posts/{id}")
async def delete_post(id:int, db: session = Depends(get_db)):
    # PSYCOPG2 implementation of delete_post
    """ cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone() """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Used with in memory data
'''
def find_post(id : int, iterator:List):
    return next((x for x in iterator if x["id"] == id), None)

def find_post_index(id : int, iterator:List):
    return next((i for i,x in enumerate(iterator) if x["id"] == id), None)
'''