from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

app = FastAPI()

class Post(BaseModel):
    title : str = Field(title="Post title")
    content : str
    published : bool = True

while True:
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
        time.sleep(2)
    
    

# posts = [{"id":1, "title":"First post", "content":"Contet test"},
#                      {"id":2, "title":"Second post", "content":"Pizza is the best!"}]

@app.get("/")
async def hello():
    return {"message": "Hello api"}

@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) 
                   VALUES (%s,%s,%s) RETURNING * ''', (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.get('/posts/{id}') 
async def get_post(id: int): # response: Response
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} was not found"} """
    return {"data": post}


@app.put("/posts/{id}")
async def update_post(id:int, post: Post):
    
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s
                    RETURNING *""",
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    conn.commit()
    return{"data": updated_post}


@app.delete("/posts/{id}")
async def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Used with in memory data
'''
def find_post(id : int, iterator:List):
    return next((x for x in iterator if x["id"] == id), None)

def find_post_index(id : int, iterator:List):
    return next((i for i,x in enumerate(iterator) if x["id"] == id), None)
'''