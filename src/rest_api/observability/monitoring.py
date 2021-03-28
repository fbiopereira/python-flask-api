from flask_restplus import Resource, fields
from flask import Response
from src.rest_api.api import api
from src.rest_api.observability.namespace import ns_observability
from prometheus_client import generate_latest
from src.app import flask_app, log


@ns_observability.route('/metrics')
@api.response(200, 'Prometheus Metrics')
class Metrics(Resource):

    def get(self):
        return Response(generate_latest())


@ns_observability.route('/healthcheck')
@api.response(200, 'Liveness status')
class Liveness(Resource):

    def get(self):
        return Response("I'm alive")


info_model = ns_observability.model('InfoReturnModel', {
                    'ENVIRONMENT': fields.String(),
                    'SERVICE_NAME': fields.String(),
                    'SERVICE_VERSION': fields.String(),
                    'SERVER_DATETIME': fields.String(),
                    'ENVIRONMENT VARIABLES': fields.String(),
                })

@ns_observability.route('/info')
@api.response(200, 'Environment info')
class Info(Resource):

    @ns_observability.marshal_with(info_model)
    def get(self):
        info_return = {
            "version": get_service_version(),
            "environment": app.flask_app.config['ENVIRONMENT'],
            "server_datetime": get_server_datetime(),
            "environment_variables": [
                {"LOG_PATH": app.flask_app.config['LOG_PATH']},
                {"SERVICE_NAME": app.flask_app.config['SERVICE_NAME']}
            ]
        }

        return info_return, 200

