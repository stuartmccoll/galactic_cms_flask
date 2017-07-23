# from datetime import datetime

from application.init_app import db, manager
# from application.models.user import User


@manager.command
def init_db():
    """ Initialize the database."""
    # Create all tables
    db.create_all()
    # Add all Users
    # add_users()


# def add_users():
#     find_or_create_user(u'Admin', u'Example', u'admin@example.com',
#                         'Password1')
#     db.session.commit()


# def find_or_create_user(first_name, last_name, email, password):
#     """ Find existing user or create new user """
#     user = User.query.filter(User.email == email).first()
#     if not user:
#         user = User(email=email,
#                     first_name=first_name,
#                     last_name=last_name,
#                     password=password,
#                     active=True,
#                     confirmed_at=datetime.datetime.utcnow())
#         db.session.add(user)
#     return user
