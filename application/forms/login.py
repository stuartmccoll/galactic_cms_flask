from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from application.models.user import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """
        Validates user login credentials provided.
        :param self: The current LoginForm object.
        :returns: A Boolean indicating whether or not validation
                  was successful.
        """
        if FlaskForm.validate(self):
            user = User.query.filter_by(username=self.username.data).first()
            if user and user.validate_login(
                user.password, str(self.password.data)
            ):
                self.user = user
                return True

        self.username.errors.append(f"Invalid login credentials provided")
        return False
