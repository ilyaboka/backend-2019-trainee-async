import magic
from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import form_schema
from aiohttp_apispec import response_schema

from exceptions import InputValidationError
from exceptions import UnsupportedMediaType
from integrations import GoogleSpeechToText
from schemas import RecognizeRequestSchema
from schemas import RecognizeResponseSchema


@docs(
    tags=['Speech-To-Text'], summary='Распознать речь', description='Распознавание речи через Google Speech-To-Text',
)
@form_schema(RecognizeRequestSchema)
@response_schema(RecognizeResponseSchema)
async def recognize(request):
    """Распознать речь"""
    request_data: bytes = request['form']['speechFile'].file.read()

    if not request_data:
        raise InputValidationError('Empty body')

    if magic.from_buffer(request_data, mime=True) not in [
        # pylint: disable=bad-continuation
        'audio/flac',
        'audio/x-wav',
    ]:
        # pylint: enable=bad-continuation
        raise UnsupportedMediaType('Invalid speech file')

    return web.json_response(dict(recognizedText=await GoogleSpeechToText.recognize(request_data),))
