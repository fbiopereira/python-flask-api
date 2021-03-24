

class BaseError(BaseException):
    """
    Base package for errors.
    """
    def __init__(self, code, message, friendly_message, http_status):
        """
        :param code: error reference
        :param message: message to support
        :param friendly_message: user-friendly message
        :param http_status: valid http code
        """
        self.code = code
        self.message = message
        self.friendly_message = friendly_message
        self.http_status = http_status

    def get_friendly_message_json(self):
        return {
            "error_code": self.code,
            "message": self.friendly_message,
            "response": ""
        }

    def get_error_json(self):
        return {
            "error_code": self.code,
            "message": self.message,
            "friendly_message": self.friendly_message,
            "http_status": self.http_status
        }
