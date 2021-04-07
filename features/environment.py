# http://behave.readthedocs.io/en/latest/tutorial.html#works-in-progress

# Fixtures simplify the setup/cleanup tasks that are often needed during test execution.

# -- FILE: behave4my_project/fixtures.py  (or in: features/environment.py)
from behave import fixture
# from somewhere.browser.firefox import FirefoxBrowser
import httpretty
# -- FIXTURE: Use generator-function
@fixture
def browser_firefox(context, timeout=30, **kwargs):
    # -- SETUP-FIXTURE PART:
    # context.browser = FirefoxBrowser(timeout, **kwargs)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.shutdown()


def before_step(centext, step):
    pass


def after_step(context, step):
    pass


def before_scenario(context, scenario):
    httpretty.enable()
    pass


def after_scenario(context, scenario):
    httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
    httpretty.reset()
    if hasattr(context, 'patch'):
        context.patch.stop()


def before_all(context):
    pass

