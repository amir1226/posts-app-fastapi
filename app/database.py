from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_psw}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
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