from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from application.models.user import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Invalid login credentials provided \
                                        \nPlease try again')
            return False

        if not user.validate_login(user.password, str(self.password.data)):
            self.username.errors.append('Invalid login credentials')
            return False

        self.user = user
        return True
