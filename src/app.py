import os
from infra import CustomLog
from helpers import get_service_version
from flask import Flask, Blueprint
from .settings import Settings
from prometheus_flask_exporter import PrometheusMetrics


settings = Settings()

flask_app = Flask(__name__)
metrics = PrometheusMetrics(flask_app)
log = CustomLog(get_service_version(), service_name=os.environ.get('SERVICE_NAME'))




def initialize_app(flask_app):
    settings.configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(flask_app)

    log.info(class_name="app.py", method="main", message="Starting {0} application in {1} environment"
             .format(flask_app.config["SERVICE_NAME"], flask_app.config["ENVIRONMENT"]))

    flask_app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()