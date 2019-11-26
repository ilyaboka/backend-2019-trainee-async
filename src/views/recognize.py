import magic
from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import response_schema

from exceptions import InputValidationError
from exceptions import UnsupportedMediaType
from integrations import GoogleSpeechToText
from schemas import RecognizeResponseSchema


@docs(
    tags=['Speech-To-Text'], summary='Распознать речь', description='Распознавание речи через Google Speech-To-Text',
)
@response_schema(RecognizeResponseSchema)
async def recognize(request):
    """Распознать речь"""
    request_data: bytes = await request.read()

    if not request_data:
        raise InputValidationError('Empty body')

    if magic.from_buffer(request_data, mime=True) not in [
        'audio/flac',
        'audio/x-wav',
    ]:
        raise UnsupportedMediaType('Invalid speech file')

    return web.json_response(dict(recognizedText=await GoogleSpeechToText.recognize(request_data),))
