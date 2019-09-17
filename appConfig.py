# Import flask and template operators
import os

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import config
from instance.config import app_config

# Define the database object which is imported
db = SQLAlchemy()

flask_bcrypt = Bcrypt()

def initialize_app(config_name):
    

    # Define the WSGI application object
    app = Flask(__name__)

    
    # Configurations
    app.config.from_object('config')
    app.config.from_object(app_config[config_name])
    
    # ..DEBUG
    # Build the database:
    # This will create the database file using SQLAlchemy by preparing it to use app
    db.init_app(app)

    #provides bcrypt hashing utilities for your application.
    flask_bcrypt.init_app(app)


    return app
