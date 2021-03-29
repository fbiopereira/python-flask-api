from flask_restplus import Resource
from app.custom_log.log_request import log_request
from .namespace import ns_observability



@ns_observability.route('/healthcheck')
class Liveness(Resource):

    @log_request
    @ns_observability.response(200, 'Liveness status')
    def get(self):
        return "I'm alive", 200