# EESBS API

## Overview

This project is a basic overview of an backend api involving user authentication and profile defination.

## Technology Used

1. Flask
2. flask-restplus
3. Flask-SQLAlchemy
4. gunicorn
5. PyJWT
6. bcrypt

## Installation and set-up

1. Clone the project - git clone <https://github.com/bafiam/EESBS.git>
2. create a virtual environment using virtualenv.
3. Install the dependencies - pip install -r requirements.txt.

## Run the server

1. Next is to start the server with the command python run.py.
2. The server should be running on [localhost](http://127.0.0.1:5000)

## API Modules

API Module | Functionality 
------------ | -------------
Auth| Provide user authentication using jwt token.url_prefix='/api/v1/auth'
profile| Allow authenticated users to add/edit their profile. url_prefix='/api/v1/profile'

## online access

To access the online version on Heroku
1. User auth module [heroku](https://eesbs.herokuapp.com/api/v1/auth/)
2. User profile module [heroku](https://eesbs.herokuapp.com/api/v1/profile/)

## Author

**Stephen Gumba**
