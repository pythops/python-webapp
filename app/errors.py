from fastapi.responses import JSONResponse

from app import exceptions


def error_handler(app):
    @app.exception_handler(exceptions.UserAlreadyExists)
    async def http_409(request, exception):
        return JSONResponse(status_code=409, content={"error": str(exception)})
