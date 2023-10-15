class BaseException(Exception):
    message: str

    def __init__(self, message=None, **kwargs):
        super().__init__(message or self.message)
        self.kwargs = kwargs


class UserAlreadyExists(BaseException):
    message = "User Already Exists"
