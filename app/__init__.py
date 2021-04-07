from .settings import flask_app, log, service_version, api
from .rest_api.observability import Liveness
from .rest_api.observability.namespace import ns_observability
from .rest_api.movies_v1.namespace import ns_movies_v1
from .rest_api.movies_v2.namespace import ns_movies_v2


api.init_app(flask_app)
api.add_namespace(ns_observability, path="/monit")
api.add_namespace(ns_movies_v1, path="/movies/v1")
api.add_namespace(ns_movies_v2, path="/movies/v2")



def main():
    log.info(message="Starting flask application")
    flask_app.run()
