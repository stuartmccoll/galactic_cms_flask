import os

DBUSER = 'galactic'
DBPASS = 'password'
DBHOST = 'database'
DBPORT = '5432'
DBNAME = 'testdb'

SECRET_KEY = os.urandom(24)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
