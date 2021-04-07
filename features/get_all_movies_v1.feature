Feature: Get All movies


  Scenario: I will get movies in a Mongodb but database is empty
    Given I clear mongodb
    When get request to api/movies/v1/movie is received
    Then should return status code 200 OK
    Then the the API will return the following json
    """
    {
      "total_movies": 0,
      "movies": []
    }
    """

  Scenario: I will get movies in a Mongodb with 3 movies
    Given I register log handler
    Given I clear mongodb
    Given I save a movie in the mongodb
    """
    {
      "title": "1-Star Wars VI - The Empire Strikes Back",
      "genre": "adventure",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    Given I save a movie in the mongodb
    """
    {
      "title": "2-Star Wars VI - The Empire Strikes Back",
      "genre": "adventure",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    Given I save a movie in the mongodb
    """
    {
      "title": "3-Star Wars VI - The Empire Strikes Back",
      "genre": "adventure",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    When get request to api/movies/v1/movie is received
    Then should return status code 200 OK
    Then the the API will return the following json
    """
    {
      "total_movies": 3,
      "movies": [
        {
          "title": "1-Star Wars VI - The Empire Strikes Back",
          "genre": "adventure",
          "director": "Irvin Kershner",
          "story": "George Lucas",
          "release_year": 1980
        },
        {
          "title": "2-Star Wars VI - The Empire Strikes Back",
          "genre": "adventure",
          "director": "Irvin Kershner",
          "story": "George Lucas",
          "release_year": 1980
        },
        {
          "title": "3-Star Wars VI - The Empire Strikes Back",
          "genre": "adventure",
          "director": "Irvin Kershner",
          "story": "George Lucas",
          "release_year": 1980
        }
      ]
    }
    """
    Then info log line containing Found 3 movie(s) in database is produced