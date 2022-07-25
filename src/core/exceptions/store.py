from core.exceptions.base import MethodNotAllowed


class OrderDoesNotExists(MethodNotAllowed):
    message = "Order does not exists"


class OrderAlreadyExists(MethodNotAllowed):
    message = "Order already exists"


class StatusDoesNotCorrect(MethodNotAllowed):
    message = "Status does not correct"
