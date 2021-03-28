import os
from src.helpers.git_helpers import GitHelpers
from src.custom_log.custom_log import CustomLog


class Settings:

    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.configure_environment()
        self.git_helpers = GitHelpers(self.environment)
        self.service_version = self.git_helpers.get_service_version()

        self.configure_flask()
        self.log = CustomLog(service_name=flask_app.config['SERVICE_NAME'],
                        service_version=flask_app.config['SERVICE_VERSION'],
                        environment=flask_app.config['ENVIRONMENT'], log_path=self.log_path)

    def configure_environment(self):
        if os.environ.get('FLASK_DEBUG') is not None:
            self.flask_debug = os.environ.get('FLASK_DEBUG')
        else:
            self.flask_debug = True  # Do not use debug mode in production


        self.restplus_swagger_ui_doc_expansion = 'list'
        self.restplus_validate = True
        self.restplus_mask_swagger = False
        self.restplus_error_404_help = False


        if os.environ.get('SERVICE_NAME') is not None:
            self.service_name = os.environ.get('SERVICE_NAME')
        else:
            self.service_name = "NOME_DO_SERVICO_NAO_INFORMADO"

        if os.environ.get('ENVIRONMENT') is not None:
            self.environment = os.environ.get('ENVIRONMENT')
        else:
            self.environment = "development"
            self.flask_debug = True
        if os.environ.get('LOG_PATH') is not None:
            self.log_path = os.environ.get('LOG_PATH')
        else:
            self.log_path = None

    def configure_flask(self):
        self.flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = self.restplus_swagger_ui_doc_expansion
        self.flask_app.config['RESTPLUS_VALIDATE'] = self.restplus_validate
        self.flask_app.config['RESTPLUS_MASK_SWAGGER'] = self.restplus_mask_swagger
        self.flask_app.config['ERROR_404_HELP'] = self.restplus_error_404_help
        self.flask_app.config['ENVIRONMENT'] = self.environment
        self.flask_app.config['SERVICE_NAME'] = self.service_name
        self.flask_app.config['SERVICE_VERSION'] = self.service_version







