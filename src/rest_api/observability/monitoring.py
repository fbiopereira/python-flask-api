from flask_restplus import Resource, fields
from flask import Response
from src.rest_api.api import api
from src.rest_api.observability.namespace import ns_observability
from prometheus_client import generate_latest
from src.custom_log.log_request import log_request
from src.app import flask_app
from src.helpers.datetime_helpers import DateTimeHelpers


@ns_observability.route('/metrics')
@api.response(200, 'Prometheus Metrics')
class Metrics(Resource):

     def get(self):
         return Response(generate_latest())


@log_request
@ns_observability.route('/healthcheck')
@api.response(200, 'Liveness status')
class Liveness(Resource):

    def get(self):
        return Response("I'm alive"), 200


info_model = ns_observability.model('InfoReturnModel', {
                    'ENVIRONMENT': fields.String(),
                    'SERVICE_NAME': fields.String(),
                    'SERVICE_VERSION': fields.String(),
                    'SERVER_DATETIME': fields.String(),
                    'ENVIRONMENT VARIABLES': fields.String(),
                 })


@log_request
@ns_observability.route('/info')
@api.response(200, 'Environment info')
class Info(Resource):

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
