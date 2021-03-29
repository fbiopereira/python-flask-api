from app.custom_errors.base_error import BaseError
from app.custom_errors.general_unexpected_error import GeneralUnexpectedError
from app.settings import log

class ErrorHelpers:

    @staticmethod
    def check_exceptions(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except BaseError as ex:
                log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                              http_status=ex.http_status, message=ex.message)
                return ex.get_friendly_message_json(), ex.http_status
            except Exception as ex:
                ex = GeneralUnexpectedError(app.flask_app.config['SERVICE_NAME'], str(ex))
                log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                              http_status=ex.http_status, message=ex.message)
                return ex.get_friendly_message_json(), ex.http_status

        return wrapper
