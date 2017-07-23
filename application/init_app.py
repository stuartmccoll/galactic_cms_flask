from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import logging

import config as app_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=app_config.DBUSER,
        passwd=app_config.DBPASS,
        host=app_config.DBHOST,
        port=app_config.DBPORT,
        db=app_config.DBNAME)
app.config['SECRET_KEY'] = app_config.SECRET_KEY

db = SQLAlchemy()
ma = Marshmallow(app)
manager = Manager(app)


def init_app(app, extra_config_settings={}):

    db.init_app(app)

    # Setup Flask-Migrate
    migrate = Migrate(app, db)  # noqa
    manager.add_command('db', MigrateCommand)

    from application.models.user import User  # noqa

    import application.manager_commands  # noqa
