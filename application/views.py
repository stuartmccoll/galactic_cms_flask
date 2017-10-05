from datetime import datetime
from flask import render_template, request, redirect, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, \
                        login_required, current_user
import base64
import json
import os

from init_app import app, db, logger
from models.post import Posts
from models.user import User
from models.user_profile import UserProfile
from forms.post import PostForm
from forms.login import LoginForm
from forms.user_settings import UserSettingsForm


login_manager = LoginManager()
login_manager.init_app(app)
# Return the show_login function if the user has not been authenticated
login_manager.login_view = 'show_login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/')
def show_home():
    response = json.loads(get_latest_post())
    latest_post = response['latest_post']

    response = json.loads(get_latest_posts(5))
    if response:
        latest_posts = response

    return render_template('themes/active/index.html', latest_post=latest_post,
                           latest_posts=latest_posts)


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
            featured_image = base64.b64encode(form.featured_image.data.read())
            post = Posts(title=form.title.data,
                         content=form.content.data,
                         featured_image=featured_image,
                         date_posted=datetime.now(),
                         user_id=current_user.get_id(),)
            logger.info('Creating a New Post with the title "%s" for user %s'
                        % (form.title.data, current_user.get_id()))
            db.session.add(post)
            db.session.commit()
            return json.dumps({'status': 'success'})
        logger.error('Create Post failed for user %s' % current_user.get_id())
        return json.dumps({'status': 'failure'})


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

    response = json.loads(get_previous_post(post.id))
    previous_post = response['previous_post']

    response = json.loads(get_next_post(post.id))
    next_post = response['next_post']

    response = json.loads(get_latest_post())
    latest_post = response['latest_post']

    response = json.loads(get_latest_posts(5))
    latest_posts = response

    return render_template('post.html', post=post, previous_post=previous_post,
                           next_post=next_post, latest_post=latest_post,
                           latest_posts=latest_posts)


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
        featured_image = returned_post.featured_image
        return render_template('edit-post.html', id=id, form=form,
                               featured_image=featured_image)
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
    form = UserSettingsForm()
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_profile = UserProfile.query.filter_by(id=user.user_profile_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not user_profile:
                logger.info('Creating new user settings for user %s'
                            % current_user.get_id())
                user_profile = UserProfile(id=current_user.get_id(),
                                           first_name=form.first_name.data,
                                           last_name=form.last_name.data)
                user.user_profile_id = current_user.get_id()
            if user_profile:
                logger.info('Updating user settings for user %s'
                            % current_user.get_id())
                user_profile.first_name = form.first_name.data
                user_profile.last_name = form.last_name.data
            db.session.add(user_profile)
            db.session.commit()
            return 'User settings updated successfully', 200
        return json.dumps({'status': 'failure'})
    if request.method == 'GET':
        logger.info('Retrieving User Settings screen for user %s'
                    % current_user.get_id())
        if user_profile:
            form.first_name.data = user_profile.first_name
            form.last_name.data = user_profile.last_name
        return render_template('user-settings.html', form=form)


@app.route('/admin/site-config')
@login_required
def site_config():

    user = User.query.filter_by(id=current_user.get_id()).first()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    logger.info('Current directory path is %s' % dir_path)
    if dir_path == '/app/application':
        logger.info('Checking that themes directory exists for user \
                     %s' % user.id)
        if os.path.exists(dir_path + '/templates/themes'):
            logger.info('Checking that themes exist for user %s' % user.id)
            themes = os.walk(dir_path + '/templates/themes').next()[1]
            logger.info('Found the following themes for user %s: \
                         %s' % (user.id, themes))

            theme_dict = {}

            for theme in themes:
                logger.info('Checking that theme folder %s has a\
                             config.json file' % theme)

                theme_with_config = os.path.exists(dir_path + '/templates/themes/' + theme + '/config.json')
                if theme_with_config:
                    logger.info('Found config.json file for theme folder %s'
                                % theme)

                    theme_dict[str(theme)] = {}

                    with open(dir_path + '/templates/themes/' + theme
                              + '/config.json') as theme_config:
                        data = json.load(theme_config)

                        theme_dict[theme]['name'] = data['theme']['name']
                        theme_dict[theme]['description'] = data['theme']['description']
                        theme_dict[theme]['author'] = data['theme']['author']
                        theme_dict[theme]['author_website'] = data['theme']['author-website']
                        theme_dict[theme]['config_name'] = data['theme']['config-name']
                        theme_dict[theme]['directory_name'] = theme
                        if theme == "active":
                            theme_dict[theme]['active'] = True
                        else:
                            theme_dict[theme]['active'] = False

                else:
                    logger.info('Did not find config.json file \
                                for theme folder %s' % theme)

            logger.info(theme_dict)

    return render_template('site-configuration.html', themes=theme_dict)


@app.route('/admin/themes/activate/<theme_name>', methods=['POST'])
@login_required
def activate_theme(theme_name):

    dir_path = get_working_directory()
    user = User.query.filter_by(id=current_user.get_id()).first()

    if get_working_directory():
        logger.info('Checking that themes directory exists for user \
                     %s' % user.id)
        if os.path.exists(dir_path + '/templates/themes'):

            # Get config.json for active theme
            get_config = os.path.exists(dir_path + '/templates/themes/active/config.json')
            if get_config:
                # Load config.json
                with open(dir_path + '/templates/themes/active/config.json') as theme_config:
                    data = json.load(theme_config)
                    os.rename(dir_path + '/templates/themes/active', dir_path + '/templates/themes/' + data['theme']['config-name'])

            # Get config.json for theme to activate
            get_config = os.path.exists(dir_path + '/templates/themes/' + theme_name + '/config.json')
            if get_config:
                # Load config.json
                with open(dir_path + '/templates/themes/' + theme_name + '/config.json') as theme_config:
                    data = json.load(theme_config)
                    os.rename(dir_path + '/templates/themes/' + theme_name, dir_path + '/templates/themes/active')

    return jsonify({"status": "success"}), 200


def get_working_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logger.info('Current directory path is %s' % dir_path)
    if dir_path == '/app/application':
        return dir_path
    return False


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


def get_latest_posts(number):
    returned_posts = db.session.query(Posts).order_by(Posts.id.desc()) \
        .limit(number).all()

    if returned_posts:
        latest_posts = {}
        for posts in returned_posts:
            logger.info(posts)
            latest_posts[posts.id] = {
                "title": posts.title,
                "featured_image": str(posts.featured_image)
            }

        return json.dumps(latest_posts)
    return json.dumps({"latest_posts": False})


def get_latest_post():
    returned_post = db.session.query(Posts).order_by(Posts.id.desc()).first()
    if returned_post:
        return json.dumps({"latest_post": returned_post.id})
    return json.dumps({"latest_post": False})


def get_next_post(current_post):
    returned_post = Posts.query.filter(Posts.id > current_post).first()

    if returned_post:
        logger.info("next %s" % returned_post)
        return json.dumps({"next_post": returned_post.id})
    return json.dumps({"next_post": False})


def get_previous_post(current_post):
    returned_post = Posts.query.filter(Posts.id < current_post).first()

    if returned_post:
        logger.info("previous %s" % returned_post)
        return json.dumps({"previous_post": returned_post.id})
    return json.dumps({"previous_post": False})
