Feature: Get All movies

  @wip
  Scenario: I will get movies in a real Mongodb but database is empty
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
