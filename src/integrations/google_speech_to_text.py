from base64 import b64encode

from aiohttp import ClientError
from aiohttp import ClientResponse
from aiohttp import ClientSession

from exceptions import MessageSendingException
from exceptions import ServerError
from settings import GOOGLE_API_KEY
from settings import GOOGLE_SPEECH_TO_TEXT_URL


class GoogleSpeechToTextException(ServerError):
    ...


class GoogleSpeechToText:
    @staticmethod
    async def get_transcript_from_response(response: ClientResponse) -> str:
        """ Get transcript text from Google REST API Response """
        try:
            print(await response.json())
            transcript: str = (await response.json())['results'][0]['alternatives'][0]['transcript']
            return transcript
        except KeyError as key_error:
            raise GoogleSpeechToTextException("Can't make request to Google Speech-To-Text") from key_error

    @classmethod
    async def recognize(cls, audio_file: bytes) -> str:
        """ Return transcript for speech in audiofile """
        try:
            async with ClientSession() as session:
                async with session.post(
                    # pylint: disable=bad-continuation
                    GOOGLE_SPEECH_TO_TEXT_URL,
                    params=dict(key=GOOGLE_API_KEY,),
                    json=dict(
                        audio=dict(content=b64encode(audio_file).decode('ascii'),), config=dict(languageCode='en-US',),
                    ),
                ) as response:
                    # pylint: enable=bad-continuation
                    return await cls.get_transcript_from_response(response)
        except ClientError as client_error:
            raise MessageSendingException("Can't make request to Google Speech-To-Text") from client_error
        except UnicodeDecodeError as unicode_decode_error:
            raise GoogleSpeechToTextException("Can't make request to Google Speech-To-Text") from unicode_decode_error
