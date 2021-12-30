from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

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
    class Config:
        orm_mode = True
        
class CreateUser(BaseModel):
    email : EmailStr
    password : str
    
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