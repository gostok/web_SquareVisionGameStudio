import os
import time
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from wtforms import StringField
from werkzeug.utils import secure_filename
from flask import url_for

from app.routers.home_app.models import Image

# Папка для загрузки изображений
UPLOAD_FOLDER = "app/static/img"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Создаем директорию для загрузки, если она не существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class BlogPostModelView(ModelView):
    form_extra_fields = {
        "image_url": FileUploadField("Image", base_path=UPLOAD_FOLDER),
        "user_id": StringField("User   ID"),
    }

    def generate_unique_filename(self, filename):
        """Генерирует уникальное имя для файла, добавляя временную метку."""
        base, extension = os.path.splitext(filename)
        unique_filename = f"{base}_{int(time.time())}{extension}"
        return unique_filename

    def save_image(self, image, upload_folder):
        """Сохраняет изображение в указанную папку и возвращает относительный путь."""
        filename = secure_filename(image.filename)

        if not Image.is_valid_extension(filename):
            raise ValueError("Invalid file extension.")

        # Генерируем уникальное имя файла
        unique_filename = filename
        file_path = os.path.join(upload_folder, unique_filename)

        # Проверка на существование файла и генерация уникального имени
        while os.path.exists(file_path):
            unique_filename = self.generate_unique_filename(filename)
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
        model = super().create_model(form)

        if model is None:  # Проверяем, была ли модель создана
            return model  # Возвращаем None, если не удалось создать

        if form.image_url.data:
            # Сохраняем изображение и обновляем путь
            relative_path = self.save_image(form.image_url.data, UPLOAD_FOLDER)
            model.image_url = relative_path
            print("relative_path in create_model:" + relative_path)

        return model

    def edit_model(self, form, model):
        """Обрабатывает загрузку файла при редактировании."""
        if form.image_url.data:
            # Сохраняем изображение и обновляем путь
            relative_path = self.save_image(form.image_url.data, UPLOAD_FOLDER)
            model.image_url = relative_path
            print("relative_path in edit_model:" + relative_path)

        return super().edit_model(form, model)
