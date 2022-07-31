from core.exceptions.base import (ConflictException, NotFoundException,
                                  UnauthorizedException)


class UserWithSameEmailExists(ConflictException):
    message = "User with same email exists"


class UserWithSameLoginExists(ConflictException):
    message = "User with same login exists"


class UserWithSamePhoneExists(ConflictException):
    message = "User with same phone exists"


class UserDoesNotExists(NotFoundException):
    message = "User does not exists"


class PasswordOrLoginDoesNotMatch(UnauthorizedException):
    pass
