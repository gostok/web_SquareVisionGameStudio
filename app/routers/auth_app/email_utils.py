from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel


class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str


conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",  # имя пользователя (адрес электронной почты), с которого будут отправляться письма.
    MAIL_PASSWORD="your_password",  # пароль для этого адреса электронной почты.
    MAIL_FROM="your_email@example.com",  # тот же адрес электронной почты, с которого отправляются письма.
    MAIL_PORT=587,  # порт, используемый для подключения к SMTP-серверу (587 — стандартный порт для SMTP с TLS).
    MAIL_SERVER="smtp.example.com",  # адрес SMTP-сервера, который будет использоваться для отправки писем.
    MAIL_FROM_NAME="Your Name",  # имя отправителя, которое будет отображаться в письме.
    MAIL_TLS=True,  # параметры, определяющие, следует ли использовать TLS или SSL для защищенного соединения.
    MAIL_SSL=False,
)


async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email],
        body=email.message,
        subtype="html",
    )
    fm = FastMail(config=conf)
    await fm.send_message(message=message)
