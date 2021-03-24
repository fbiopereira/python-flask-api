import os


class Settings:

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

    def configure_app(self, app_flask):
        app_flask.config['SWAGGER_UI_DOC_EXPANSION'] = self.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
        app_flask.config['RESTPLUS_VALIDATE'] = self.RESTPLUS_VALIDATE
        app_flask.config['RESTPLUS_MASK_SWAGGER'] = self.RESTPLUS_MASK_SWAGGER
        app_flask.config['ERROR_404_HELP'] = self.RESTPLUS_ERROR_404_HELP
        app_flask.config['ENVIRONMENT'] = self.ENVIRONMENT
        app_flask.config['SERVICE_NAME'] = self.SERVICE_NAME

        return app_flask



