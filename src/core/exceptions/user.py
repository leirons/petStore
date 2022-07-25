from core.exceptions.base import MethodNotAllowed, UnauthorizedException


class UserWithSameEmailExists(MethodNotAllowed):
    message = "User with same email exists"


class UserWithSameLoginExists(MethodNotAllowed):
    message = "User with same login exists"


class UserWithSamePhoneExists(MethodNotAllowed):
    message = "User with same phone exists"


class UserDoesNotExists(MethodNotAllowed):
    message = "User does not exists"


class PasswordOrLoginDoesNotMatch(UnauthorizedException):
    pass
