import os
from app.helpers.git_helpers import GitHelpers
from app.custom_log import CustomLog
from flask import Flask
from flask_restplus import Api
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics

flask_app = Flask(__name__)

# Setting environment variables

environment = "development"
if os.environ.get('ENVIRONMENT') is not None:
    environment = os.environ.get('ENVIRONMENT')

flask_debug = True
if os.environ.get('FLASK_DEBUG') is not None:
    flask_debug = os.environ.get('FLASK_DEBUG')

if environment != "development":
    flask_debug = False

if flask_debug is None:
    flask_debug = True  # Do not use debug mode in production

service_name = "NOME_DO_SERVICO_NAO_INFORMADO"
if os.environ.get('SERVICE_NAME') is not None:
    service_name = os.environ.get('SERVICE_NAME')

genre_service_url = ""
if os.environ.get('GENRE_SERVICE_URL') is not None:
    genre_service_url = os.environ.get('GENRE_SERVICE_URL')

movie_notify_service_url = ""
if os.environ.get('MOVIE_NOTIFY_SERVICE_URL') is not None:
    movie_notify_service_url = os.environ.get('MOVIE_NOTIFY_SERVICE_URL')

mongo_uri = "mongodb://localhost:27017/movies"
if os.environ.get('MONGO_URI') is not None:
    mongo_uri = os.environ.get('MONGO_URI')

log_path = None
if os.environ.get('LOG_PATH') is not None:
     log_path = os.environ.get('LOG_PATH')

# Setting restplus variables

restplus_swagger_ui_doc_expansion = 'list'
restplus_validate = True
restplus_mask_swagger = False
restplus_error_404_help = False
git_helpers = GitHelpers(environment)
service_version = git_helpers.get_service_version()

# Setting flask config variables

flask_app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ['get', 'post']
flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = restplus_swagger_ui_doc_expansion
flask_app.config['RESTPLUS_VALIDATE'] = restplus_validate
flask_app.config['RESTPLUS_MASK_SWAGGER'] = restplus_mask_swagger
flask_app.config['ERROR_404_HELP'] = restplus_error_404_help
flask_app.config['ENVIRONMENT'] = environment
flask_app.config['SERVICE_NAME'] = service_name
flask_app.config['SERVICE_VERSION'] = service_version
flask_app.config['LOG_PATH'] = log_path
flask_app.config['MONGO_URI'] = mongo_uri
flask_app.config['GENRE_SERVICE_URL'] = genre_service_url
flask_app.config['MOVIE_NOTIFY_SERVICE_URL'] = movie_notify_service_url

log = CustomLog(service_name=service_name,
                service_version=service_version,
                environment=environment, log_path=log_path)


metrics = PrometheusMetrics(flask_app)

api = Api(title='Flask Restplus API', version=service_version,
          description='A Flask RestPlus boilerplate to be used in my demos', doc="/", prefix="/api", validate=True)

mongodb = PyMongo(flask_app)





