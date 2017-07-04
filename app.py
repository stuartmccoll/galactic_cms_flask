from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, login_user, logout_user, login_required

from models.user import User
from datetime import datetime

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

db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Create random users for testing purposes - TODO: Remove this
users = [User(id) for id in range(1, 21)]


@login_manager.user_loader
def load_user(userid):
    return User(userid)


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
        self.user_id = 2

    def __repr__(self):
        return '<Posts : id=%r, title=%s, content=%s>' \
                % (self.id, self.title, self.content)


class PostsSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'content', 'date_posted', 'user_id')


posts_schema = PostsSchema()
posts_schema = PostsSchema(many=True)

db.create_all()


@app.route('/admin')
@login_required
def show_admin():
    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['login-username']
        password = request.form['login-password']
        # TODO: Remove the next conditional - this is here for testing purposes
        if password == username:
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            session['user_id'] = id
            return redirect('/admin')


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'GET':
        return render_template('create-post.html')
    if request.method == 'POST':
        post = Posts(title=request.form['post-title'],
                     content=request.form['post-content'], date_posted='a',
                     user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        return 'Post created successfully', 200


@app.route('/view-posts')
@login_required
def view_posts():
    return render_template('view-posts.html')


@app.route('/get-posts')
@login_required
def get_posts():
    results = db.session.query(Posts) \
              .filter_by(user_id=session['user_id']).all()
    return posts_schema.jsonify(results)


@app.route('/delete-post/<id>')
@login_required
def delete_post(id):
    db.session.query(Posts).filter_by(id=id,
                                      user_id=session['user_id']).delete()
    db.session.commit()
    return 'Post deleted successfully', 200


@app.route('/edit-post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    returned_post = db.session.query(Posts) \
                    .filter_by(id=id, user_id=session['user_id']).first()
    if request.method == 'GET':
        return render_template('edit-post.html', title=returned_post.title,
                               content=returned_post.content, id=id)
    if request.method == 'POST':
        returned_post.title = request.form['post-title']
        returned_post.content = request.form['post-content']
        db.session.commit()
        return 'Post updated successfully', 200


@app.route('/user-settings')
@login_required
def user_settings():
    return render_template('user-settings.html')


@app.route('/site-config')
@login_required
def site_config():
    return render_template('site-configuration.html')


@app.route('/raise-support-ticket')
@login_required
def raise_support_ticket():
    return render_template('raise-support-ticket.html')


@app.route('/help')
@login_required
def show_help():
    return render_template('help.html')


@app.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
