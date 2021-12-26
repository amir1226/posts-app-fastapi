from fastapi import FastAPI, HTTPException
from .database import engine, get_db
from . import models, utils
from .routers import post, user


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


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

@app.get("/")
async def hello():
    return {"message": "Hello api"}
