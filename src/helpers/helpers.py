from flask import request
from app.custom_error import *
from hamcrest import *
import app
from threading import Thread
from git import Repo, TagReference
import os
from datetime import datetime

def check_json(json_expected, json_response):
    if type(json_expected) is list:
        for i in range(0, len(json_expected)):
            check_json(json_expected[i], json_response[i])
            check_json(json_response[i], json_expected[i])
    elif type(json_expected) is dict:
        for key, value in json_expected.items():
            if type(value) is dict:
                assert_that(json_response, has_key(key))
                check_json(value, json_response[key])
                check_json(json_response[key], value)
            elif type(value) is list:
                for i in range(0, len(value)):
                    check_json(json_expected[key][i], json_response[key][i])
                    check_json(json_response[key][i], json_expected[key][i])
            else:
                assert_that(json_response, has_entry(key, value))
    else:
        assert_that(json_response, equal_to(json_expected))


def check_exceptions(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BaseError as ex:
            app.log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                          http_status=ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status
        except Exception as ex:
            ex = GeneralUnexpectedError(app.flask_app.config['SERVICE_NAME'], str(ex))
            app.log.error(code=ex.code, class_name='helpers', method='check_exceptions',
                          http_status=ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status

    return wrapper


def build_response(error_code, message, response, status_code):
    return {
        "error_code": error_code,
        "message": message,
        "response": response
    }, status_code


def build_working_response(service, status, error_description='', error_code=''):
    return {
        "service": service,
        "status": status,
        "error_description": error_description,
        "error_code": error_code
    }


def log_request(f):
    def wrapper(*args, **kwargs):
        message = "Method: " + str(request.method) + " endpoint: " + request.full_path + " body: "
        if request.data:
            message += str(request.data)

        app.log.info(class_name='helpers', method='log_request',
                     http_status=200, message='Request recebido: ' + message)
        response = f(*args, **kwargs)
        return response
    return wrapper


def process_async(async_function):
    def decorator(f):
        def wrapper(*args, **kwargs):
            thread = Thread(target=async_function, args=args, kwargs=kwargs)
            thread.start()
            return f(*args, **kwargs)
        return wrapper
    return decorator


def get_git_repo():
    git_path = os.path.dirname(os.path.abspath(__file__))
    if os.name != 'nt':
        git_path = git_path.replace("/app/helpers", "")
    else:
        git_path = git_path.replace("\\app\\helpers", "")
    repo = Repo(git_path)
    return repo

def get_git_last_commit():
    return str(get_git_repo().head.commit)

def get_git_last_tag():
    try:
        tag_ref = TagReference.list_items(get_git_repo())[0]
        if tag_ref.tag is not None:
            return str(tag_ref.tag)
        else:
            return 'n0.0.0'
    except Exception:
        return 'e0.0.0'

def get_service_version():
    if app.config_name != 'production':
        return get_git_last_commit()
    else:
        return get_git_last_tag()

def get_server_datetime():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt

