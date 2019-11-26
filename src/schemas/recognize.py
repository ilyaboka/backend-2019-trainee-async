from marshmallow import Schema
from marshmallow import fields


class RecognizeRequestSchema(Schema):
    speechFile: fields.Raw = fields.Field(
        description='Аудиофайл, содержащий речь для распознования', location="form", required=True, type='file',
    )


class RecognizeResponseSchema(Schema):
    recognizedText: fields.Str = fields.Str(
        description='Распознанный текст', required=True,
    )
