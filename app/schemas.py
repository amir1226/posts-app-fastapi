from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from pydantic.types import conint


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True  

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class PostBase(BaseModel):
    title : str = Field(title="Post title")
    content : str    
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True
        
class CreateUser(BaseModel):
    email : EmailStr
    password : str
    
class Vote(BaseModel):
    post_id : int
    dir: conint(ge=0,le=1)