import os
import time
import uuid
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from wtforms import StringField
from werkzeug.utils import secure_filename
from flask import url_for

from app.routers.home_app.models import Image
from app.routers.auth_app.models import User  # Импортируем модель User


# Папка для загрузки изображений
UPLOAD_FOLDER = "app/static/img"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Создаем директорию для загрузки, если она не существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlogPostModelView(ModelView):
    form_extra_fields = {
        "image_url": FileUploadField("Image", base_path=UPLOAD_FOLDER),
        "username": StringField("Username"),  # Убедитесь, что здесь нет лишнего пробела
    }

    def generate_random_filename(self, extension):
        """Генерирует уникальное имя для файла с использованием UUID."""
        unique_filename = f"{uuid.uuid4()}.{extension}"
        return unique_filename

    def save_image(self, image, upload_folder):
        """Сохраняет изображение в указанную папку и возвращает относительный путь."""
        filename = secure_filename(image.filename)

        if not Image.is_valid_extension(filename):
            raise ValueError("Invalid file extension.")

        # Получаем расширение файла
        extension = filename.rsplit(".", 1)[1].lower()
        # Генерируем уникальное имя файла
        unique_filename = self.generate_random_filename(extension)
        file_path = os.path.join(upload_folder, unique_filename)

        # Сохраняем файл под уникальным именем
        try:
            image.save(file_path)  # Сохраняем файл
            return f"img/{unique_filename}"  # Возвращаем только относительный путь
        except Exception as e:
            raise ValueError(
                f"Error saving file: {e}"
            )  # Обработка ошибок при сохранении файла

    def create_model(self, form):
        """Создает модель и сохраняет изображение."""
        logger.info("Attempting to create model with form data: %s", form.data)

        model = super().create_model(form)

        if model is False:  # Проверяем, была ли модель успешно создана
            logger.error("Failed to create model: %s", form.errors)
            return None  # Возвращаем None, если не удалось создать

        if form.image_url.data:
            # Сохраняем изображение и обновляем путь
            relative_path = self.save_image(form.image_url.data, UPLOAD_FOLDER)
            model.image_url = relative_path

        # Установка username, если он передан
        if form.username.data:

            model.username = form.username.data

        return model

    def edit_model(self, form, model):
        """Обрабатывает загрузку файла при редактировании."""
        if form.image_url.data:
            # Сохраняем изображение и обновляем путь
            relative_path = self.save_image(form.image_url.data, UPLOAD_FOLDER)
            model.image_url = relative_path

        # Установка username, если он передан
        if form.username.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                model.user_id = user.id  # Устанавливаем user_id для модели

        return super().edit_model(form, model)
