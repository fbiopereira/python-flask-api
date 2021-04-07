from flask import request
import app


def log_request(f):
    def wrapper(*args, **kwargs):
        message = "Method: " + str(request.method) + " endpoint: " + request.full_path + " body: "
        if request.data:
            message += str(request.data)

        app.log.info(message='Request recebido: ' + message)
        response = f(*args, **kwargs)
        return response
    return wrapper
