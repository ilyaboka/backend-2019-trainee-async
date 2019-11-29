from typing import Any
from typing import Dict

import magic
from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from exceptions import InputValidationError
from exceptions import UnsupportedMediaType


class RecognizeRequestSchema(Schema):
    speechFile: fields.Raw = fields.Raw(
        description='Аудиофайл, содержащий речь для распознования', location="form", required=True, type='file',
    )

    @post_load
    def check_speech_file(  # pylint: disable=no-self-use,unused-argument
        # pylint: disable=bad-continuation
        self,
        item: Dict[str, Any],
        many: bool,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # pylint: enable=bad-continuation
        """Проверить mime-type присланного аудиофайла"""
        speech_file_data: bytes = item['speechFile'].file.read()

        if not speech_file_data:
            raise InputValidationError('Empty file')

        magic_type: str = magic.from_buffer(speech_file_data, mime=True)
        if magic_type not in [
            # pylint: disable=bad-continuation
            'audio/flac',
            'audio/x-wav',
        ]:
            # pylint: enable=bad-continuation
            raise UnsupportedMediaType(f'Invalid speech file type: {magic_type}')

        item['speechFile'] = speech_file_data
        return item


class RecognizeResponseSchema(Schema):
    recognizedText: fields.Str = fields.Str(
        description='Распознанный текст', required=True,
    )
