from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

app = FastAPI()

class Post(BaseModel):
    title : str = Field(title="Post title")
    content : str
    published : bool = True

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
    
except Exception as error:
    print('Connecciont to database failed\nError: ', error)
    
    

posts = [{"id":1, "title":"First post", "content":"Contet test"},
                      {"id":2, "title":"Second post", "content":"Pizza is the best!"}]

@app.get("/")
async def hello():
    return {"message": "Hello api"}

@app.get("/posts")
async def get_posts():
    return {"posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 1000000)
    posts.append(post_dict)
    return {"data": post_dict}

@app.get('/posts/{id}') 
async def get_post(id: int): # response: Response
    post = find_post(id, posts)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
        """ response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id {id} was not found"} """
    return {"data": post}


@app.put("/posts/{id}")
async def update_post(id:int, updated_post: Post):
    post_index = find_post_index(id, posts)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    updated_post = updated_post.dict()
    updated_post["id"] = id
    posts[post_index] = updated_post
    return{"data": updated_post}


@app.delete("/posts/{id}")
async def delete_post(id:int):
    post_index = find_post_index(id, posts)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def find_post(id : int, iterator:List):
    return next((x for x in iterator if x["id"] == id), None)

def find_post_index(id : int, iterator:List):
    return next((i for i,x in enumerate(iterator) if x["id"] == id), None)