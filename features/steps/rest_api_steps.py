import json
from behave import Given, Then, When
from hamcrest import assert_that, equal_to
from json_helpers import check_json
import httpretty
import app


@Given('the request will receive the following json body')
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@When('{method} request to {url} is received')
def json_request(context, method, url):
    data = None
    headers = {}
    content_type = 'application/json'

    if 'json_body' in context:
        data = json.dumps(context.json_body)

    if hasattr(context, 'mock_configurations'):
        for mock_configuration in context.mock_configurations:
            httpretty.register_uri(method=mock_configuration['method'].upper(), uri=mock_configuration['url'],
                                   status=mock_configuration['status'], body=mock_configuration['body'],
                                   match_querystring=True)

    client = app.flask_app.test_client()

    response = getattr(client, method)(url, data=data, content_type=content_type, headers=headers)
    context.response = response
    try:
        context.response.json = json.loads(context.response.data)
    except Exception:
        pass


@Then('the the API will return the following json')
def return_json(context):
    result = context.response.json
    check_json(json.loads(context.text), result)


@Then('should return status code {status_code} {status_name}')
def response_status_code(context, status_code, status_name):
    assert_that(context.response.status_code, equal_to(int(status_code)))
