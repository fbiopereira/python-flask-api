from flask_restplus import Resource, fields
from app.helpers.error_helpers import ErrorHelpers
from app.helpers.json_encoder import JSONEncoder
from app.custom_log import log_request
from app.custom_errors.general_unexpected_error import GeneralUnexpectedError
from .namespace import ns_movies_v2
from flask import request
import json
import requests
from app.settings import log, service_name, flask_app, mongodb


@ns_movies_v2.route("/movie")
class MovieApiV2(Resource):
    @log_request
    @ErrorHelpers.check_exceptions
    def get(self):
        return self.list_all_movies()

    @log_request
    @ErrorHelpers.check_exceptions
    def post(self):
        json_body = request.json
        return self.save_new_movie(json_body)

    def save_new_movie(self, json_body):
        try:
            log.info(200, message="Starting saving new movie v2 in database with json {}".format(str(json_body)))
            genre = self.get_genre(json_body["genre"])
            movie_json = json_body
            movie_json['genre'] = genre

            movies_db = mongodb.db.movies
            movies_db.insert_one(movie_json)

            log.info(
                201,
                message="Saved new movie in database with document {}".format(JSONEncoder().encode(movie_json)))

            api_return = json.loads(str(JSONEncoder().encode(movie_json)))
            del api_return['_id']
            self.movie_notify(api_return)
            return api_return, 201
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

    def get_genre(self, genre_id):
        service_url = flask_app.config['GENRE_SERVICE_URL'] + "/api/genre/" + str(genre_id)
        log.info(200, message="Starting to request genre at {0}".format(service_url))
        genre_response = requests.get(service_url)
        if genre_response.status_code == 200:
            return genre_response.json()["genre"]
        else:
            return "genre not found"

    def movie_notify(self, movie):
        service_url = flask_app.config['MOVIE_NOTIFY_SERVICE_URL'] + "/api/movie-notify"
        log.info(200, message="Starting to request genre at {0}".format(service_url))
        response = requests.post(service_url, json=movie)
        if response.status_code == 200:
            return True
        else:
            return False