from core.exceptions.base import ConflictException, NotFoundException
from resources.strings import (OrderAlreadyExistsMessage,
                               OrderDoesNotFoundMessage)


class OrderDoesNotFound(NotFoundException):
    message = OrderDoesNotFoundMessage


class OrderAlreadyExists(ConflictException):
    message = OrderAlreadyExistsMessage
