"""
The config module is meant to hold the configurations for the deployment of
the flask application.
"""

import os

DEBUG = True

DB_TYPE = 'mysql+pymysql'
DB_SERVER = os.environ['DB_SERVER']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_DATABASE = os.environ['DB_DATABASE']
DB_PORT = os.environ['DB_PORT']

SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}'
