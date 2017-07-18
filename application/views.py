from datetime import datetime
from flask import render_template, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, \
                        login_required, current_user
# from flask_marshmallow import Marshmallow
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
# from flask_sqlalchemy import SQLAlchemy

from init_app import app, db
from models.post import Posts, posts_schema
from models.user import User
from models.user_profile import UserProfile


login_manager = LoginManager()
login_manager.init_app(app)
# Return the show_login function if the user has not been authenticated
login_manager.login_view = 'show_login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/admin')
@login_required
def show_admin():
    posts = db.session.query(Posts) \
              .filter_by(user_id=current_user.get_id()) \
              .order_by(Posts.date_posted.desc()).limit(5)
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_profile = UserProfile.query.filter_by(id=user.user_profile_id) \
        .first()
    return render_template('admin.html', all_posts=posts,
                           user=user, user_profile=user_profile)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['login-username']
        password = request.form['login-password']
        user = User.query.filter_by(username=username).first()
        if user and User.validate_login(user.password, str(password)):
            login_user(user)
            return redirect('/admin')
        flash("Invalid login credentials provided\nPlease try again",
              category='error')
        return render_template('login.html')


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'GET':
        return render_template('create-post.html')
    if request.method == 'POST':
        post = Posts(title=request.form['post-title'],
                     content=request.form['post-content'],
                     date_posted=datetime.now(),
                     user_id=current_user.get_id())
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
              .filter_by(user_id=current_user.get_id()).all()
    return posts_schema.jsonify(results)


@app.route('/delete-post/<id>')
@login_required
def delete_post(id):
    db.session.query(Posts).filter_by(id=id, user_id=current_user.get_id()) \
                                      .delete()
    db.session.commit()
    # TODO Change return based on the outcome of the delete
    return 'Post deleted successfully', 200


@app.route('/edit-post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    returned_post = db.session.query(Posts) \
                    .filter_by(id=id, user_id=current_user.get_id()).first()
    if request.method == 'GET':
        return render_template('edit-post.html', title=returned_post.title,
                               content=returned_post.content, id=id)
    if request.method == 'POST':
        returned_post.title = request.form['post-title']
        returned_post.content = request.form['post-content']
        db.session.commit()
        return 'Post updated successfully', 200


@app.route('/user-settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_profile = UserProfile.query.filter_by(id=user.user_profile_id).first()
    if request.method == 'POST':
        if not user_profile:
            user_profile = UserProfile(id=current_user.get_id(),
                                       first_name=request.form['first-name'],
                                       last_name=request.form['last-name'])
        if user_profile:
            user_profile.first_name = request.form['first-name']
            user_profile.last_name = request.form['last-name']
        db.session.add(user_profile)
        db.session.commit()
        return 'User settings updated successfully', 200
    if request.method == 'GET':
        return render_template('user-settings.html',
                               first_name=user_profile.first_name,
                               last_name=user_profile.last_name)


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
