from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))    

#SECRET KEY
SECRET_KEY = os.getenv('SECRET_KEY') 
#Algorithm
ALGORITHM = os.getenv('ALGORITHM') 
#Expiration Time
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

