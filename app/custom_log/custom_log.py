from datetime import datetime
import platform
import os
import glob
import logging
import logging.handlers
import logging.config
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from .json_log_formatter import JSONFormatter
import socket


class CustomLog(object):

    def __init__(self, service_name, service_version, environment, log_path=None, scope_name=__name__):

        self._max_file_size = 500000
        self._log_folder = None
        self.service_name = service_name
        self.service_version = os.getenv('GIT_TAG', service_version)
        self.service_ip = socket.gethostbyname(socket.gethostname())
        self.environment = os.getenv('ENVIRONMENT', environment)
        self.formatter = JSONFormatter()
        self._logger = logging.getLogger(scope_name)

        if log_path is not None:
            self._log_folder = log_path
            self.create_log_file()

        self.create_stdout_handler()

        self._logger.setLevel(logging.DEBUG)

    def create_folder(self):
        if not os.path.exists(self._log_folder):
            os.makedirs(self._log_folder)

    def create_log_file(self):
        self.create_folder()
        file_name = datetime.now().strftime('%d-%m-%Y.{}_log').format(self.service_name.replace(" ", "_"))
        file_path = "{0}{1}".format(self._log_folder, file_name)

        file_handler = RotatingFileHandler(
            file_path, maxBytes=self._max_file_size, backupCount=20)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)

        self._logger.addHandler(file_handler)

    def create_stdout_handler(self):
        stream_handler = StreamHandler()
        stream_handler.setFormatter(self.formatter)
        stream_handler.setLevel(logging.DEBUG)

    def path(self):
        """Return the path of the logs folder.
        For default, path is your folder.
        """
        return self._log_folder

    def service_name_log(self):
        """service name that used in info, warning and error."""
        return self.service_name

    def service_version_log(self):
        """service version thats used in info, warning and error."""
        return self.service_version

    def count_log_files(self):
        """Return number of custom_log files."""
        return len(glob.glob("{0}/*.custom_log*".format(self._log_folder)))

    def get_log_files(self):
        """Return all logs files."""
        return glob.glob("{0}/*.custom_log*".format(self._log_folder))

    def delete_log_files(self):
        for file in glob.glob("{0}/*.custom_log*".format(self._log_folder)):
            try:
                os.remove(file)
            except IOError:
                self.error("erro ao excluir")

    def debug(self, message):
        self._logger.debug(message)

    def info(self, correlation_id=None, message=None):

        self._logger.info(
            message, extra={'level': 'INFO',
                            'service_name': self.service_name, 'service_version': self.service_version,
                            'service_ip': self.service_ip, 'environment': self.environment,
                            'so_version': platform.release(), 'python_version': platform.python_version(),
                            'correlation_id': correlation_id})

    def warning(self, correlation_id=None, message=None):

        self._logger.warning(
            message, extra={'level': 'WARNING',
                            'service_name': self.service_name, 'service_version': self.service_version,
                            'service_ip': self.service_ip, 'environment': self.environment,
                            'so_version': platform.release(), 'python_version': platform.python_version(),
                            'correlation_id': correlation_id})

    def error(self, correlation_id=None, message=None, exception=None, error_code=None, friendly_message=None,
              http_status=None):

        self._logger.error(
            message, extra={'level': 'ERROR',
                            'service_name': self.service_name, 'service_version': self.service_version,
                            'service_ip': self.service_ip, 'environment': self.environment,
                            'so_version': platform.release(), 'python_version': platform.python_version(),
                            'correlation_id': correlation_id, 'exception': exception, 'error_code': error_code,
                            'friendly_message': friendly_message, 'http_status': http_status
                            }, exc_info=True)
