from core.exceptions.base import MethodNotAllowed,UnauthorizedException


class UserExists(MethodNotAllowed):
    message = "Пользователь с таким логином или емайлом уже существует"

class PasswordOrLoginDoesNotMatch(UnauthorizedException):
    pass