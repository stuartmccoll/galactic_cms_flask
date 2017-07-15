from datetime import datetime

from application.init_app import db, ma


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, content, date_posted, user_id):
        self.title = title
        self.content = content
        self.date_posted = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<Posts : id=%r, title=%s, content=%s>' \
                % (self.id, self.title, self.content)


class PostsSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'content', 'date_posted', 'user_id')


posts_schema = PostsSchema()
posts_schema = PostsSchema(many=True)
