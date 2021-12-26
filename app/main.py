from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import session
from .database import engine, get_db
from . import models, utils
from .schemas import PostCreate, PostResponse, CreateUser, UserResponse



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/posts", response_model=list[PostResponse])
async def get_posts(db: session = Depends(get_db)):
    # PSYCOPG2 implementation of get_posts
    """cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall() """
    
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: session = Depends(get_db)):
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
    return new_post

@app.get('/posts/{id}', response_model=PostResponse) #response_model_include/exclude= {} or []
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
    return post


@app.put("/posts/{id}", response_model=PostResponse)
async def update_post(id:int, post: PostCreate, db: session = Depends(get_db)):
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
    return post_query.first()


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


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user: CreateUser, db: session = Depends(get_db)):
    
    #Hash password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
   
@app.get('/users/{id}', response_model=UserResponse)
async def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    return user
    
    
# Used with in memory data
'''
def find_post(id : int, iterator:List):
    return next((x for x in iterator if x["id"] == id), None)

def find_post_index(id : int, iterator:List):
    return next((i for i,x in enumerate(iterator) if x["id"] == id), None)
'''