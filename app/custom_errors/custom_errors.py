class AppError(Exception):
    def __init__(self, message:str) -> None:
        self.message=message

class RepositoryError(AppError):
       pass

class NotFoundException(AppError):
    pass

class AlreadyExistException(AppError):
     pass