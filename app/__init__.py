from fastapi import FastAPI
from app.database import db

from app.config import config


def init_app():
    api = FastAPI()
    db.init(uri=config.DB_URI)

    from app.errors import error_handler
    from app.api import routes

    api.include_router(routes.router)

    error_handler(api)

    return api
