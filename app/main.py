from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database.db import *

from app.routers.auth_app.routes import router_auth
from app.routers.home_app.routes import router_home
from app.admin_flask.admin import admin


Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
app.mount("/uploads", StaticFiles(directory="database/uploads"), name="uploads")


app.include_router(router_home, prefix="", tags=["home"])
app.include_router(router_auth, prefix="/auth", tags=["auth"])
app.mount("/admin", admin.app)
