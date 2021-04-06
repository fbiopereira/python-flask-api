Feature: Save movies v2


  Scenario: I will save a movie in a mocked Mongodb
    Given I set the environment variable GENRE_SERVICE_URL to http://localhost:1432
    Given I set the environment variable MOVIE_NOTIFY_SERVICE_URL to http://localhost:1433
    Given the request will receive the following json body
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": 1,
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    Given I mock a GET method sent to GENRE_SERVICE_URL to endpoint /api/genre/1 will return status code 200 and the following json
    """
    {
      "id": 1,
      "genre": "adventure from genre service",
      "description": "a movie with lots of adventure",
      "parental_guidance": "PG13"
    }
    """
    Given I mock a POST method sent to MOVIE_NOTIFY_SERVICE_URL to endpoint /api/movie-notify will return status code 200 and the following json
    """
    """
    When post request to api/movies/v2/movie is received
    Then the following document is saved mongodb
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": "adventure from genre service",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    Then should return status code 201 CREATED
    Then the the API will return the following json
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": "adventure from genre service",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    Then the last request received by the mock in the endpoint /api/movie-notify has body
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": "adventure from genre service",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
