import threading

from flask import Flask
from fastapi import FastAPI

from app.main import app
from app.admin_flask.admin import flask_app


def run_flask():
    flask_app.run(port=5000)


def run_fastapi():
    import uvicorn

    uvicorn.run(app=app, host="127.0.0.1", port=8000)


from fastapi import UploadFile


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    fastapi_thread = threading.Thread(target=run_fastapi)

    flask_thread.start()
    fastapi_thread.start()

    flask_thread.join()
    fastapi_thread.join()
