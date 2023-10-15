from fastapi import FastAPI


def init_app():
    api = FastAPI()

    from app.errors import error_handler
    from app.api import routes

    api.include_router(routes.router)

    error_handler(api)

    return api
