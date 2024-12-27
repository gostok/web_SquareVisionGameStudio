from fastapi import APIRouter, Depends, HTTPException, Request, Response, Body
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

from app.routers.auth_app.models import User
from app.routers.auth_app.schemas import UserCreate
from app.config import security, config
from database.db import get_db

# from app.routers.auth_app.email_utils import send_email, EmailSchema  # для отправки подтверждения email


router_auth = APIRouter()
templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router_auth.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("auth_temp/login.html", {"request": request})


@router_auth.get("/register", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("auth_temp/register.html", {"request": request})


@router_auth.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):

    form = await request.form()
    user_create = UserCreate(
        username=form.get("username"),
        email=form.get("email"),
        hashed_password=form.get("password"),
    )

    existing_user = (
        db.query(User)
        .filter(
            (User.username == user_create.username) | (User.email == user_create.email)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = pwd_context.hash(user_create.hashed_password)

    # Создаем нового пользователя
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        role=user_create.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # логика отправки email
    # email_data = EmailSchema(
    #     email=user_create.email,
    #     subject="Confirm your email",
    #     message="Please confirm your email by clicking on the link."
    # )
    # await send_email(email_data)

    return RedirectResponse(url="/auth/login", status_code=303)


@router_auth.post("/login")
async def login_user(
    response: Response,
    username: str = Body(...),  # Получаем username из тела запроса
    password: str = Body(...),  # Получаем password из тела запроса
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Генерация токена и установка кука
    token = security.create_access_token(user.username)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, httponly=False)

    return {"access_token": token, "username": user.username}


@router_auth.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)  # Удаление кука при выходе
    return RedirectResponse(url="/auth/login", status_code=303)
