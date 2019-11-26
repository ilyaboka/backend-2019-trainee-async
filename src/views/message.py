from typing import Dict
from uuid import uuid4

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_apispec import request_schema
from aiohttp_apispec import response_schema

from schemas import APISPEC_DEFAULT_PARAMS
from schemas import MessageCreateRequestSchema
from schemas import MessageCreateResponseSchema


@docs(
    tags=['SMS'],
    summary='Запрос отправки сообщения',
    description='Описание запроса',
    parameters=APISPEC_DEFAULT_PARAMS,
)
@request_schema(MessageCreateRequestSchema)
@response_schema(MessageCreateResponseSchema)
async def send_message(request: web.Request) -> web.Response:
    """Отправляет сообщение"""
    message_id: str = str(uuid4())
    res: Dict[str, str] = dict(
        phoneNumber=request['data']['phoneNumber'], text=request['data']['text'], messageId=message_id,
    )

    validated_games_list: Dict[str, str] = MessageCreateResponseSchema().load(res)

    response: web.Response = web.json_response(validated_games_list)

    return response
