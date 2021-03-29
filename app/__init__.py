from .settings import flask_app, log, service_version, api
from .rest_api.observability import Liveness
from .rest_api.movies_v1 import MovieApi
from .rest_api.observability.namespace import ns_observability
from .rest_api.movies_v1.namespace import ns_movies_v1




api.init_app(flask_app)
api.add_namespace(ns_observability, path="/monit")
api.add_namespace(ns_movies_v1, path="/movies/v1")

def main():
    log.info(message="Starting flask application")
    flask_app.run()
