from marshmallow import Schema
from marshmallow import fields


class RecognizeRequestSchema(Schema):
    speechFile: fields.Raw = fields.Raw(required=True, description='Аудиофайл, содержащий речь для распознования')


class RecognizeResponseSchema(Schema):
    recognizedText: fields.Str = fields.Str(required=True, description='Распознанный текст')
