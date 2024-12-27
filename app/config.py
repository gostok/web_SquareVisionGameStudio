import os
from dotenv import load_dotenv

from authx import AuthX, AuthXConfig

load_dotenv()

# ------------------------------------------------------------------------------

# JWT_TOKEN & COOKIE
config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_MAX_AGE = 86400  # 24 часа работы куков
config.JWT_COOKIE_SAMESITE = "Lax"  # Политика SameSite для куков | "Lax" позволяет кукам отправляться в запросах, инициированных с других сайтов, но только для безопасных методов (например, GET)
config.JWT_COOKIE_SECURE = False  # True - Использовать только по HTTPS в продакшене

security = AuthX(config=config)

# ------------------------------------------------------------------------------
