Feature: Save movies v1

  Scenario: I will save a movie in a real Mongodb
    Given I clear mongodb
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
    Given a get method to genre service to endpoint /api/genre/1 will return the following json
    """
    {
      "id": 1,
      "genre": "adventure from genre service",
      "description": "a movie with lots of adventure",
      "parental_guidance": "PG13"
    }
    """
    When post request to api/movies/v1/movie is received
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
      "genre": "adventure from adventure service",
      "director": "Irvin Kershner",
      "story": "George Lucas",
      "release_year": 1980
    }
    """
