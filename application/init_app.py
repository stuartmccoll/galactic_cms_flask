import logging

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

import config as app_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.debug = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg2://{app_config.DBUSER}:{app_config.DBPASS}@{app_config.DBHOST}:{app_config.DBPORT}/{app_config.DBNAME}"
app.config["SECRET_KEY"] = app_config.SECRET_KEY

db = SQLAlchemy()
manager = Manager(app)


def init_app(app, extra_config_settings={}):

    db.init_app(app)

    # Setup Flask-Migrate
    migrate = Migrate(app, db)  # noqa
    manager.add_command("db", MigrateCommand)

    from application.models.user import User  # noqa

    import application.manager_commands  # noqa
