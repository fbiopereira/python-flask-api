from base_error import BaseError


class GeneralUnexpectedError(BaseError):
    def __init__(self, service_name, message):
        super().__init__(
            code="GUE000",
            message="Erro inesperado no {0}: {1}".format(service_name, message),
            friendly_message="Erro inesperado no {}.".format(service_name),
            http_status=500)

