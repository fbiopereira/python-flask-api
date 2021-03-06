import json
from datetime import datetime
from behave import Given, Then
from json_helpers import check_json
import mongomock
from app import settings


@Given('I save a movie in mongodb')
def save_in_mongo(context):
    json_job = json.loads(context.text)
    json_job['operation_started'] = datetime.strptime(json_job['operation_started'], '%Y-%m-%dT%H:%M:%SZ')
    json_job['job_metadata']['metadata_created_at'] = datetime.strptime(json_job['job_metadata']['metadata_created_at'],
                                                                        '%Y-%m-%dT%H:%M:%SZ')
    settings.mongodb.db.jobs.insert(json_job)


@Given('I clear mongodb')
def clear_mongo(context):
    settings.mongodb.db.movies.delete_many({})


@Then('the following document is saved mongodb')
def check_mongodb_document(context):
    movie = settings.mongodb.db.movies.find_one({}, {'_id': 0})
    expected_document = json.loads(context.text)
    check_json(json_expected=expected_document, json_to_search=movie)


@Given('I save a movie in the mongodb')
def json_sve_mock(context):
    movie = json.loads(context.text)
    settings.mongodb.db.movies.insert(movie)
    context.movie_id = movie['_id']




