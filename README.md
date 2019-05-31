# coa_flask_app

The flask back-end REST APIs for the COA website.

## Getting Started

1. Install python3.7 and pipenv.
    - `sudo apt install python3.7`
    - `sudo python3.7 -m pip install pipenv`
2. Setup DB related environment variables (not posted here for security reasons).
3. Clone down the project.
4. Start server
    - `make run`

## Testing

To test that the flask app is running and properly connected to the database,
use the curl command.

- `curl localhost:5000/locations`

Or to hit the deployed instance.

- `curl http://coa-flask-app-dev.us-east-1.elasticbeanstalk.com/locations`
