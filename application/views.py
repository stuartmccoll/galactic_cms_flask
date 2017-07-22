from datetime import datetime
from flask import render_template, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, \
                        login_required, current_user

from init_app import app, db, logger
from models.post import Posts
from models.user import User
from models.user_profile import UserProfile
from forms.login import LoginForm
from forms.create_post import PostForm


login_manager = LoginManager()
login_manager.init_app(app)
# Return the show_login function if the user has not been authenticated
login_manager.login_view = 'show_login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/admin/dashboard')
@login_required
def show_admin():
    posts = db.session.query(Posts) \
              .filter_by(user_id=current_user.get_id()) \
              .order_by(Posts.date_posted.desc()).limit(5)
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_profile = UserProfile.query.filter_by(id=user.user_profile_id) \
        .first()
    logger.info('Retrieving administrator dashboard for user_id: %s' % user.id)
    return render_template('admin.html', all_posts=posts,
                           user=user, user_profile=user_profile)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    form = LoginForm()
    if request.method == 'GET':
        logger.info('Retrieving login screen')
        return render_template('login.html', form=form)
    if request.method == 'POST':
        logger.info('Attempting login for user %s' % form.username.data)
        if form.validate_on_submit():
            login_user(form.user)
            logger.info('Login successful for user %s' % form.user.username)
            return redirect('/admin/dashboard')
        flash("Invalid login credentials provided\nPlease try again",
              category='error')
        logger.error('Login failed for username %s' % form.username.data)
        return render_template('login.html', form=form)


@app.route('/admin/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'GET':
        logger.info('Retrieving Create New Post screen for user %s'
                    % current_user.get_id())
        return render_template('create-post.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Posts(title=form.title.data,
                         content=form.content.data,
                         date_posted=datetime.now(),
                         user_id=current_user.get_id())
            logger.info('Creating a New Post with the title "%s" for user %s'
                        % (form.title.data, current_user.get_id()))
            db.session.add(post)
            db.session.commit()
            return 'Post created successfully', 200
        logger.error('Create Post failed for user %s' % current_user.get_id())


@app.route('/admin/view-posts')
@login_required
def view_posts():
    posts = db.session.query(Posts) \
              .filter_by(user_id=current_user.get_id()) \
              .order_by(Posts.date_posted.desc())
    logger.info('Retrieving View Posts screen for user %s'
                % current_user.get_id())
    return render_template('view-posts.html', posts=posts)


@app.route('/post/<id>')
def view_post(id):
    post = db.session.query(Posts).filter_by(id=id).first()
    return render_template('post.html', post=post)


@app.route('/admin/delete-post/<id>')
@login_required
def delete_post(id):
    logger.info('Processing delete-post request for user %s and post %s'
                % (current_user.get_id(), id))
    db.session.query(Posts).filter_by(id=id, user_id=current_user.get_id()) \
        .delete()
    db.session.commit()
    # TODO Change return based on the outcome of the delete
    return 'Post deleted successfully', 200


@app.route('/admin/edit-post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostForm()
    returned_post = db.session.query(Posts) \
        .filter_by(id=id, user_id=current_user.get_id()).first()
    if request.method == 'GET':
        logger.info('Retrieving Edit Post screen for user %s and post %s' %
                    (current_user.get_id(), id))
        form.title.data = returned_post.title
        form.content.data = returned_post.content
        return render_template('edit-post.html', id=id, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            returned_post.title = form.title.data
            returned_post.content = form.content.data
            logger.info('Updating post %s for user %s' %
                        (id, current_user.get_id()))
            db.session.commit()
            return 'Post updated successfully', 200


@app.route('/admin/user-settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_profile = UserProfile.query.filter_by(id=user.user_profile_id).first()
    if request.method == 'POST':
        if not user_profile:
            logger.info('Creating new user settings for user %s'
                        % current_user.get_id())
            user_profile = UserProfile(id=current_user.get_id(),
                                       first_name=request.form['first-name'],
                                       last_name=request.form['last-name'])
        if user_profile:
            logger.info('Updating user settings for user %s'
                        % current_user.get_id())
            user_profile.first_name = request.form['first-name']
            user_profile.last_name = request.form['last-name']
        db.session.add(user_profile)
        db.session.commit()
        return 'User settings updated successfully', 200
    if request.method == 'GET':
        logger.info('Retrieving User Settings screen for user %s'
                    % current_user.get_id())
        return render_template('user-settings.html',
                               first_name=user_profile.first_name,
                               last_name=user_profile.last_name)


@app.route('/admin/site-config')
@login_required
def site_config():
    return render_template('site-configuration.html')


@app.route('/admin/raise-support-ticket')
@login_required
def raise_support_ticket():
    return render_template('raise-support-ticket.html')


@app.route('/admin/help')
@login_required
def show_help():
    return render_template('help.html')


@app.route('/admin/sign-out')
@login_required
def sign_out():
    logout_user()
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
