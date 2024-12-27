from pydantic import BaseModel, HttpUrl
from uuid import UUID
from datetime import datetime


class BlogPostBase(BaseModel):
    title: str
    content: str
    image_url: HttpUrl | None = None


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostSchema(BlogPostBase):
    id: str
    published_at: datetime
    user_id: str
    username: str

    class Config:
        orm_mode = True
