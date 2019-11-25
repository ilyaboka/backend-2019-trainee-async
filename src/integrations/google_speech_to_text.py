from base64 import b64encode
from exceptions import ServerError
from http import HTTPStatus
from typing import Optional

from aiohttp import ClientError
from aiohttp import ClientResponse
from aiohttp import ClientSession

from settings import GOOGLE_API_KEY
from settings import GOOGLE_SPEECH_TO_TEXT_URL


class GoogleSpeechToTextException(ServerError):
    def __init__(
        # pylint: disable=bad-continuation
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        payload: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        # pylint: enable=bad-continuation
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        self.status_code: int = status_code if status_code else HTTPStatus.INTERNAL_SERVER_ERROR.value
        self.title: Optional[str] = title
        self.payload: Optional[str] = payload
        super().__init__(detail, exception_code)


class GoogleSpeechToText:
    @staticmethod
    async def get_transcript_from_response(response: ClientResponse) -> str:
        """ Get transcript text from Google REST API Response """
        try:
            transcript: str = await response.json()['results'][0]['alternatives'][0]['transcript']
            return transcript
        except KeyError as key_error:
            raise GoogleSpeechToTextException(response.text) from key_error

    @classmethod
    async def recognize(cls, audio_file: bytes, persistent_session: ClientSession) -> str:
        """ Return transcript for speech in audiofile """
        try:
            async with persistent_session.post(
                # pylint: disable=bad-continuation
                GOOGLE_SPEECH_TO_TEXT_URL,
                params=dict(key=GOOGLE_API_KEY,),
                data=dict(
                    audio=dict(content=b64encode(audio_file).decode('ascii'),), config=dict(languageCode='en-US',),
                ),
            ) as response:
                # pylint: enable=bad-continuation
                return cls.get_transcript_from_response(response)
        except (ClientError, UnicodeDecodeError) as exception:
            raise GoogleSpeechToTextException("Can't make request to Google Speech-To-Text") from exception
