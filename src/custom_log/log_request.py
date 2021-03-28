from flask import request
from src.app import log


def log_request(f):
    def wrapper(*args, **kwargs):
        message = "Method: " + str(request.method) + " endpoint: " + request.full_path + " body: "
        if request.data:
            message += str(request.data)

        log.info(message='Request recebido: ' + message)
        response = f(*args, **kwargs)
        return response
    return wrapper
