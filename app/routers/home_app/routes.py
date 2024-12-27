from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database.db import get_db
from app.config import security, config
from app.routers.home_app.models import BlogPost
from app.routers.home_app.schemas import BlogPostSchema


router_home = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from fastapi.staticfiles import StaticFiles


@router_home.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    blog_posts = db.query(BlogPost).order_by(BlogPost.published_at.desc()).all()
    context = {
        "request": request,
        "blog_posts": blog_posts,
    }
    return templates.TemplateResponse("home/index.html", context=context)
