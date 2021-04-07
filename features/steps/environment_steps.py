from behave import given
from app.settings import flask_app

@given('I set the environment variable {var_name} to {value}')
def step_impl(context, var_name, value):
    flask_app.config[str(var_name)] = value