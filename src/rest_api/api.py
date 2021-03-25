from flask_restplus import Api
import logging

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Flask Restplus API',
          description='A Flask RestPlus boilerplate to be used in my demos', doc="/docs")


@api.errorhandler
def default_api_error_handler(e):

    message = 'An unhandled exception occurred. Exception: {0}'.format(e)
    log.error(message)
    return {'message': message}, 500
