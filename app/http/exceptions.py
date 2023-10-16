from app.exceptions import BaseException


class NotFound(BaseException):
    message = "Not Found"


class ServiceException(BaseException):
    message = "Service exception"


class ServiceUnavailable(ServiceException):
    message = "Service unavailable"


class ServiceError(ServiceException):
    message = "Service error"


class ServiceUnauthorized(ServiceError):
    message = "Service unauthorized"


class ServiceForbidden(ServiceError):
    message = "Service forbidden"
