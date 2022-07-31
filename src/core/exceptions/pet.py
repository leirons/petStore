from core.exceptions.base import ConflictException, NotFoundException
from resources.strings import PetAlreadyExistsMessage, PetDoesNotFoundMessage


class PetDoesNotFound(NotFoundException):
    message = PetDoesNotFoundMessage


class PetAlreadyExists(ConflictException):
    message = PetAlreadyExistsMessage
