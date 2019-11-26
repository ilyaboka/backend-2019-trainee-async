from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import form_schema
from aiohttp_apispec import response_schema

from exceptions import ServerError
from integrations import GoogleSpeechToText
from schemas import RecognizeRequestSchema
from schemas import RecognizeResponseSchema


@docs(
    description='Распознавание речи через Google Speech-To-Text',
    responses={
        HTTPStatus.OK.value: {'schema': RecognizeResponseSchema, 'description': 'Успешно выполненный запрос',},
        HTTPStatus.BAD_REQUEST.value: {'schema': ServerError.get_schema(), 'description': 'Неверный запрос',},
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value: {
            'schema': ServerError.get_schema(),
            'description': 'Неверный тип аудиофайла',
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            'schema': ServerError.get_schema(),
            'description': 'Внутренняя ошибка сервера',
        },
    },
    summary='Распознать речь',
    tags=['Speech-To-Text'],
)
@form_schema(RecognizeRequestSchema)
@response_schema(RecognizeResponseSchema)
async def recognize(request: web.Request) -> web.Response:
    """Распознать речь"""
    request_data: bytes = request['form']['speechFile']

    response: web.Response = web.json_response(dict(recognizedText=await GoogleSpeechToText.recognize(request_data),))
    return response
