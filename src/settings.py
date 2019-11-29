import os
from typing import Dict

DEBUG: bool = bool(int(os.getenv('DEBUG', 1)))  # pylint: disable=invalid-envvar-default

PROJECT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APISPEC_CONF: Dict[str, str] = dict(
    title='Pitter async API',
    version='0.1',
    url='/api/pitter-async/swagger/apispec',
    swagger_path='/api/pitter-async/swagger',
    static_path='/api/pitter-async/swagger/static',
)

GOOGLE_API_KEY: str = os.environ['GOOGLE_API_KEY']

GOOGLE_SPEECH_TO_TEXT_URL: str = 'https://speech.googleapis.com/v1/speech:recognize'
