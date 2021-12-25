from pydantic import BaseModel, Field
from datetime import datetime

class PostBase(BaseModel):
    title : str = Field(title="Post title")
    content : str    
    published : bool

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
        
    class Config:
        orm_mode = True