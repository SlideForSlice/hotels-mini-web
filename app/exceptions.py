from fastapi import HTTPException, status
from sqlalchemy import delete


class Exceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)

class UserAlreadyExistsException(Exceptions):
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"

class IncorrectEmailOrPasswordException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password"


class TokenExpiredException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token expired'


class TokenAbsentException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token is missing'


class IncorrectTokenFormatException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect token format'


class UserIsNotPresentException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCanNotBeBookedException(Exceptions):
    status_code=status.HTTP_409_CONFLICT,
    detail="We have no rooms left"

class HotelAlreadyExistsException(Exceptions):
    status_code=status.HTTP_409_CONFLICT,
    detail="Hotel already exists"

class HotelIsNotPresentException(Exceptions):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Hotel not found"
