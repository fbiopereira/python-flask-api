from flask_restplus import Resource, fields
from .namespace import ns_observability
from app.custom_log.log_request import log_request
from app.helpers.datetime_helpers import DateTimeHelpers
from app.settings import flask_app

info_model = ns_observability.model('InfoReturnModel', {
                    'ENVIRONMENT': fields.String(),
                    'SERVICE_NAME': fields.String(),
                    'SERVICE_VERSION': fields.String(),
                    'SERVER_DATETIME': fields.String(),
                    'ENVIRONMENT VARIABLES': fields.String(),
                 })


@ns_observability.route('/info')
class Info(Resource):

    @log_request
    @ns_observability.response(200, 'Environment info')
    def get(self):
        info_return = {
            "version": flask_app.config['SERVICE_VERSION'],
            "environment": flask_app.config['ENVIRONMENT'],
            "server_datetime": DateTimeHelpers.get_server_datetime(),
            "environment_variables": [
                {"LOG_PATH": flask_app.config['LOG_PATH']},
                {"SERVICE_NAME": flask_app.config['SERVICE_NAME']}
             ]}

        return info_return, 200
