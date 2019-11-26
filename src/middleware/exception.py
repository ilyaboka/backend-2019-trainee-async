from typing import Awaitable
from typing import Callable
from typing import Optional

from aiohttp import web
from aiohttp import web_exceptions
from marshmallow import ValidationError as MarshmallowValidationError

import exceptions


@web.middleware
async def exception_middleware(
    # pylint: disable=bad-continuation
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.Response]],
) -> web.Response:
    # pylint: enable=bad-continuation
    """
    Обрабатывает исключения приложения
    :param request: web.Request объект запроса
    :param handler: Coroutine[[web.Request], web.Response] обработчик
    :return: web.Response объект ответа
    """
    exc: Optional[exceptions.ServerError] = None
    try:
        response: web.Response = await handler(request)
    except exceptions.ServerError as ex:
        exc = ex
    except MarshmallowValidationError as ex:
        exc = exceptions.ValidationError(debug=str(ex), message=exceptions.ValidationError.message)
    except web_exceptions.HTTPBadRequest as ex:
        exc = exceptions.InputValidationError(debug=ex.text, message=exceptions.InputValidationError.message)
    except web_exceptions.HTTPUnprocessableEntity as ex:
        exc = exceptions.ValidationError(debug=ex.text, message=exceptions.ValidationError.message)
    except web_exceptions.HTTPForbidden as ex:
        exc = exceptions.Forbidden(debug=f'Goodbye Moonmen. {ex}', message=exceptions.Forbidden.message)
    except web_exceptions.HTTPNotFound as ex:
        exc = exceptions.NotFound(debug=ex.text, message=exceptions.NotFound.message)
    except Exception as ex:  # pylint: disable=broad-except
        exc = exceptions.ServerError(debug=str(ex), message=exceptions.ServerError.message)

    if not exc:
        return response

    exc_data = exc.as_dict()
    exc_data['message'] = exc.message
    exc_data.pop('code', None)
    type(exc)(**exc_data)

    return web.json_response(exc.as_dict(), status=exc.status_code)
