from sqlalchemy import Column, String, Enum, Boolean
import enum
from uuid import uuid4

from database.db import Base


class Role(enum.Enum):
    """
    Класс Role позволяет создать перечисление (enum) для ролей пользователей.

    Роли:
        USER: Обычный пользователь, который имеет доступ к базовым функциям сайта.
        MANAGER: Менеджер, который может иметь дополнительные привилегии, например, управление контентом или пользователями.
        ADMIN: Администратор, который имеет полный доступ ко всем функциям и может управлять всеми аспектами приложения.
    """

    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), default=Role.USER)
    is_verified = Column(Boolean, default=False)
