from flask_restplus import Resource, fields
from app.helpers.error_helpers import ErrorHelpers
from app.helpers.json_encoder import JSONEncoder
from app.custom_log import log_request
from app.custom_errors.general_unexpected_error import GeneralUnexpectedError
from .namespace import ns_movies_v1
from flask import request
import json
from app.settings import log, service_name, mongodb


@ns_movies_v1.route("/movie")
class MovieApi(Resource):
    @log_request
    @ErrorHelpers.check_exceptions
    def get(self):
        return self.list_all_movies()

    @log_request
    @ErrorHelpers.check_exceptions
    def post(self):
        json_body = request.json
        return self.save_new_movie(json_body)

    def save_new_movie(self, movie_json):
        try:
            log.info(200, message="Starting saving new movie in database with json {}".format(str(movie_json)))

            movies_db = mongodb.db.movies
            movies_db.insert_one(movie_json)

            log.info(
                201,
                message="Saved new movie in database with document {}".format(JSONEncoder().encode(movie_json)))
            return json.loads(str(JSONEncoder().encode(movie_json))), 201
        except Exception as ex:
            raise GeneralUnexpectedError(service_name=service_name, message="Error saving Movie. EX: {}".format(str(ex)))

    def list_all_movies(self):
        try:
            log.info(200, message="Recovering all movies in database")

            movies_db = mongodb.db.movies
            movies_cursor = movies_db.find({})
            movie_list = []
            total_movies = 0
            for movie in movies_cursor:
                del movie['_id']
                movie_list.append(movie)
                total_movies += 1

            api_return = {
                "total_movies": total_movies,
                "movies": movie_list

            }

            log.info(200, message="Found {0} movie(s) in database". format(total_movies))

            return api_return, 200

        except Exception as ex:
            raise GeneralUnexpectedError(service_name=service_name,
                                         message="Error retrieving movies. EX: {}".format(str(ex)))