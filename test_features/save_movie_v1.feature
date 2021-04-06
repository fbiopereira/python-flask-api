Feature: Save movies v1

  Scenario: I will save a movie in a real Mongodb
    Given I clear mongodb
    Given the request will receive the following json body
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": "adventure",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
    When post request to api/movies/v1/movie is received
    Then the following document is saved mongodb
    """
    {
      "title": "Star Wars VI - The Empire Strikes Back",
      "genre": "adventure",
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
      "genre": "adventure",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
