# python-flask-api
An API made with python and flask framework to show how BDD works.

## How to run 

- Requirements:
    - Python 3.8
    - A local MongoDB

- Environment:    
    - Find the environment variables needed in settings.py
    - If you don't create any environment the software will assume default values
    - For mongodb the default url is "mongodb://localhost:27017/movies"

- Before running the app you need to use pip install requirements.txt (I suggest you to do this in a venv)
- To run the app just type "python app.py"

- Tests
  - Just type and run "behave" command
  - To know more about behave go to: https://behave.readthedocs.io/
    
- API Docs (Swagger)
  - Run the app
  - Go to /docs endpoint. Usually http://localhost:5000/docs
