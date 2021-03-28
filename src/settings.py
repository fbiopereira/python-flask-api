import os
from src.helpers.git_helpers import GitHelpers
from src.custom_log.custom_log import CustomLog


class Settings:

    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.git_helpers = GitHelpers(os.environ.get('ENVIRONMENT'))
        self.service_version = self.git_helpers.get_service_version()
        self.configure_app()
        self.log = CustomLog(service_name=flask_app.config['SERVICE_NAME'],
                        service_version=flask_app.config['SERVICE_VERSION'],
                        environment=flask_app.config['ENVIRONMENT'])

    if os.environ.get('FLASK_DEBUG') is not None:
        FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    else:
        FLASK_DEBUG = True  # Do not use debug mode in production

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    # Service settings
    SERVICE_NAME = os.environ.get('SERVICE_NAME')
    if os.environ.get('ENVIRONMENT') is not None:
        ENVIRONMENT = os.environ.get('ENVIRONMENT')
    else:
        ENVIRONMENT = "development"
        FLASK_DEBUG = True
    if os.environ.get('LOG_PATH') is not None:
        LOG_PATH = os.environ.get('LOG_PATH')
    else:
        LOG_PATH = None

    # Application Domain settings

    def configure_app(self):
        self.flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = self.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
        self.flask_app.config['RESTPLUS_VALIDATE'] = self.RESTPLUS_VALIDATE
        self.flask_app.config['RESTPLUS_MASK_SWAGGER'] = self.RESTPLUS_MASK_SWAGGER
        self.flask_app.config['ERROR_404_HELP'] = self.RESTPLUS_ERROR_404_HELP
        self.flask_app.config['ENVIRONMENT'] = self.ENVIRONMENT
        self.flask_app.config['SERVICE_NAME'] = self.SERVICE_NAME
        self.flask_app.config['SERVICE_VERSION'] = self.service_version









