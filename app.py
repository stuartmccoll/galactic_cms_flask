from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String(150))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Posts : id=%r, title=%s, content=%s>' \
                % (self.id, self.title, self.content)


class PostsSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'content')


posts_schema = PostsSchema()
posts_schema = PostsSchema(many=True)


@app.route('/admin')
def show_admin():
    return render_template('admin.html')


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        return render_template('create-post.html')
    if request.method == 'POST':
        post = Posts(title=request.form['post-title'],
                     content=request.form['post-content'])
        db.session.add(post)
        db.session.commit()
        return 'Post created successfully', 200


@app.route('/view-posts')
def view_posts():
    return render_template('view-posts.html')


@app.route('/get-posts')
def get_posts():
    results = Posts.query.all()
    return posts_schema.jsonify(results)


@app.route('/delete-post/<id>')
def delete_post(id):
    db.session.query(Posts).filter_by(id=id).delete()
    db.session.commit()
    return 'Post deleted successfully', 200


@app.route('/edit-post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    returned_post = Posts.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('edit-post.html', title=returned_post.title,
                               content=returned_post.content, id=id)
    if request.method == 'POST':
        returned_post.title = request.form['post-title']
        returned_post.content = request.form['post-content']
        db.session.commit()
        return 'Post updated successfully', 200


@app.route('/user-settings')
def user_settings():
    return render_template('user-settings.html')


@app.route('/site-config')
def site_config():
    return render_template('site-configuration.html')


@app.route('/raise-support-ticket')
def raise_support_ticket():
    return render_template('raise-support-ticket.html')


@app.route('/help')
def show_help():
    return render_template('help.html')


@app.route('/sign-out')
def sign_out():
    return render_template('sign-out.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
