import os
import logging
from flask import Flask, Blueprint
from src.settings import Settings
from prometheus_flask_exporter import PrometheusMetrics
from rest_api.api import api
from rest_api.observability.monitoring import ns_observability


flask_app = Flask(__name__)
metrics = PrometheusMetrics(flask_app)
settings = Settings(flask_app)

log = logging.getLogger(__name__)
flask_app = settings.flask_app

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(ns_observability)
flask_app.register_blueprint(blueprint)


def main():
    log.info("Starting {0} application in {1} environment"
             .format(flask_app.config["SERVICE_NAME"], flask_app.config["ENVIRONMENT"]))

    flask_app.run()


if __name__ == "__main__":
    main()
