from http import HTTPStatus

from .base import BaseAppException
from .base import ServerError


class AccessTokenInvalid(ServerError):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = 'Неверный токен'


class AuthTypeInvalid(ServerError):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = 'Неверный тип авторизации'


class InputValidationError(ServerError):
    status_code = HTTPStatus.BAD_REQUEST.value
    message = 'Некорректный запрос'


class Forbidden(ServerError):
    status_code = HTTPStatus.FORBIDDEN.value
    message = 'Доступ запрещён'


class NotFound(ServerError):
    status_code = HTTPStatus.NOT_FOUND.value
    message = 'Ресурс не найден'


class MessageSendingException(ServerError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = 'Произошла ошибка во время отправки сообщения'


class UnsupportedMediaType(ServerError):
    status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value
    message = 'Неверный тип медиафайла'


class ValidationError(ServerError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = 'Ошибка проверки данных'


__all__ = [
    'BaseAppException',
    'Forbidden',
    'ValidationError',
    'InputValidationError',
    'NotFound',
    'MessageSendingException',
    'AccessTokenInvalid',
    'AuthTypeInvalid',
]
