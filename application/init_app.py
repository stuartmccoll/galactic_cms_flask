from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

DBUSER = 'galactic'
DBPASS = 'password'
DBHOST = 'database'
DBPORT = '5432'
DBNAME = 'testdb'

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SECRET_KEY'] = 'ITSASECRET'

# Initialise Flask-SQLAlchemy
db = SQLAlchemy()
ma = Marshmallow(app)  # Initialise Flask-Marshmallow
manager = Manager(app)  # Initialise Flask-Script


def init_app(app, extra_config_settings={}):

    db.init_app(app)

    # Setup Flask-Migrate
    migrate = Migrate(app, db)  # noqa
    manager.add_command('db', MigrateCommand)

    from application.models.user import User  # noqa

    import application.manager_commands  # noqa
