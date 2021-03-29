from flask_restplus import Resource
from app.custom_log.log_request import log_request
from .namespace import ns_observability
from prometheus_client import generate_latest
from flask import Response


@log_request
@ns_observability.route('/metrics')
@ns_observability.response(200, 'Prometheus Metrics')
class Metrics(Resource):

     def get(self):
         return Response(generate_latest())