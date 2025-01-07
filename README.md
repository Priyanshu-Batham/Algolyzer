# Algolyzer - Learn AI/ML with hands on practicals.
A platform for learning about AI/ML models and algorithms from theoritical to executing pre-trained models all at one place.

## Status 
- Currently at the inital level.
- No deployments yet.
- Focusing on creating the basic structure for the project.

## How to Setup locally
- Fork and Clone the repo.
- Create a python virtual environment (recommended) and activate it.
- run `pip install -r requirements.txt`
- navigate into the main project directory `cd Algolyzer`
- run `python manage.py migrate` to create the database.
- run `python manage.py createsuperuser` this will ask you to enter some details.
- run `python manage.py runserver` to run the server on localhost:8000

## Contributing Guidelines
- Create a new branch with a suitable name for any contribution. For eg: `feature_authentication` and `fix_bug_123` are good names.
- Format the code with the bash script provided `./run_qa_format`. On windows you can manually run `black .`, `isort .` and `flake8`.
- After making the changes test your code using `python manage.py test`.
- Stage and commit your changes with a descriptive message.
- Push your changes to your forked repo and create a Pull Request(PR) with a descriptive message. If a linked issue exists, mention `fixed #<issue_number>` in the description.
- ### Note
  While commit some pre-commit hooks will run in order to check for Quality Assurance checks, it will fail if you forgot to run the `run_qa_format` or the manual steps on windows mentioned above; after this commit again.
