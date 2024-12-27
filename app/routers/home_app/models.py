from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from database.db import Base


class Image:
    def __init__(self, filename: str):
        self.filename = filename

    @property
    def url(self):
        return f"/uploads/{self.filename}"

    @staticmethod
    def is_valid_extension(filename: str) -> bool:
        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
        )


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User")

    def __init__(self, title: str, content: str, image_url: str, user_id: str):
        self.title = title
        self.content = content
        self.image_url = image_url
        self.user_id = user_id

    @property
    def image(self):
        return Image(self.image_url) if self.image_url else None
