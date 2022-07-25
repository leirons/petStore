from core.exceptions.base import MethodNotAllowed


class PetDoesNotExists(MethodNotAllowed):
    message = "Pet does not exists"


class PetAlreadyexists(MethodNotAllowed):
    message = "Pet with this id already exists"
