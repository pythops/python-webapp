from fastapi import FastAPI


def init_app():
    api = FastAPI()

    from app.api import routes

    api.include_router(routes.router)

    return api
