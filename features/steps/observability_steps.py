from behave import Given, Then
from app.settings import log
import logging


@Given('I register log handler')
def register_log_handler(context):
    context.test_log_handler = MockLoggingHandler()
    log._logger.addHandler(context.test_log_handler)


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }

@Then('{level} log line containing {log_string} is produced')
def json_sve_mock(context, level, log_string):
    found = False
    for log_line in context.test_log_handler.messages[level]:
        if log_line.find(log_string) != -1:
            found = True
            break

    assert found