from flask_restplus import Resource, fields
from app.helpers.error_helpers import ErrorHelpers
from app.helpers.json_encoder import JSONEncoder
from app.custom_log import log_request
from app.custom_errors.general_unexpected_error import GeneralUnexpectedError
from .namespace import ns_movies_v2
from flask import request
import json
from app.settings import log, mongodb, service_name


movie_model = ns_movies_v2.model('Movie Model', {
                    'title': fields.String(required=True, description="Movie Title"),
                    'genre': fields.String(required=True, description="Movie Main Genre"),
                    'director': fields.String(required=True, description="Movie Director Name"),
                    'story': fields.String(required=True, description="Movie Story Writer"),
                    'release_year': fields.Integer(required=True, description="Movie First Release Year")
                })


@ns_movies_v2.route("/movie")
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
            log.info(200, message="Starting saving new movie v2 in database with json {}".format(str(movie_json)))


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
                movie_list.append(movie)
                total_movies += 1

            api_return = {
                "total_movies": total_movies,
                "movies": movie_list

            }
            return api_return, 200

        except Exception as ex:
            raise GeneralUnexpectedError(service_name=service_name,
                                         message="Error retrieving movies. EX: {}".format(str(ex)))