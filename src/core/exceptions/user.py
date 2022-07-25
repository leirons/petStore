from core.exceptions.base import MethodNotAllowed, UnauthorizedException


class UserWithSameEmailExists(MethodNotAllowed):
    message = "Пользователь с с таким емайлом уже зарегестрирован"


class UserWithSameLoginExists(MethodNotAllowed):
    message = "Пользователь с таким логином уже зарегестрирован"


class UserWithSamePhoneExists(MethodNotAllowed):
    message = "Пользователь с таким номером телефоном уже зарегестрирован "


class UserDoesNotExists(MethodNotAllowed):
    message = "Пользователя не существует"


class PasswordOrLoginDoesNotMatch(UnauthorizedException):
    pass
