from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

import os
from dotenv import load_dotenv

from app.routers.auth_app.models import User
from app.admin_flask.model_views import BlogPostModelView
from app.routers.home_app.models import BlogPost
from database.db import SessionLocal
from app.admin_flask.admin_views import StatsView

load_dotenv()

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db = SessionLocal()

admin = Admin(flask_app, template_mode="bootstrap4")

admin.add_view(ModelView(User, db))
admin.add_view(BlogPostModelView(BlogPost, db))
admin.add_view(StatsView(name="Статистика", endpoint="stats"))
