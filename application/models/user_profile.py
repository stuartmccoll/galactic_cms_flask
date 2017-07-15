from application.init_app import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, server_default='')
    last_name = db.Column(db.String(50), nullable=False, server_default='')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User Profile : id=%r, first_name=%s, last_name=%s>' \
                % (self.id, self.first_name, self.last_name)

    def full_name(self):
        """ Return 'first_name last_name' """
        name = self.first_name
        name += ' ' if self.first_name and self.last_name else ''
        name += self.last_name
        return name
