from views import recognize
from views import send_message


def setup_routes(app):
    """Устанавливает пути запросов"""
    app.router.add_post('/api/pitter/v1/recognize', recognize)
    app.router.add_post('/api/pitter/v1/message', send_message)
