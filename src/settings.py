import os
from git import Repo, TagReference
from datetime import datetime


class Settings:

    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.configure_app()
        self.service_version = self.get_service_version()


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



    def get_git_repo(self):
        git_path = os.path.dirname(os.path.abspath(__file__))
        if os.name != 'nt':
            git_path = git_path.replace("/src", "")
        else:
            git_path = git_path.replace("\\src", "")
        repo = Repo(git_path)
        return repo

    def get_git_last_commit(self):
        return str(self.get_git_repo().head.commit)

    def get_git_last_tag(self):
        try:
            tag_ref = TagReference.list_items(self.get_git_repo())[0]
            if tag_ref.tag is not None:
                return str(tag_ref.tag)
            else:
                return 'n0.0.0'
        except Exception:
            return 'e0.0.0'

    def get_service_version(self):
        if self.flask_app.config["ENVIRONMENT"] != 'production':
            return self.get_git_last_commit()
        else:
            return self.get_git_last_tag()

    def get_server_datetime(self):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt



