from flask_login import UserMixin
from werkzeug.security import check_password_hash

from application.init_app import db
from user_profile import UserProfile  # noqa


class User(db.Model, UserMixin):

    __table_name__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False,
    #                                  server_default='')

    # Foreign Key
    user_profile_id = db.Column(db.Integer(), db.ForeignKey('user_profile.id',
                                ondelete='CASCADE'))

    user_profile = db.relationship('UserProfile',
                                   uselist=False, backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

        def __repr__(self):
            return '<User: id=%s, username=%s, email=%s>' \
                    % (self.id, self.username, self.email)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
