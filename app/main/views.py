import os, json, urllib

from flask import Blueprint, request, render_template, flash,\
    g, redirect, url_for, jsonify, make_response

from flask.ext.login import login_user, logout_user,\
    current_user, login_required

from app.main.forms import LoginForm, RegisterForm, UserForm, ProjectForm

from app import db, bcrypt, lm
from app.main.models import User, Project, Role

from flask.ext.restful import Resource, reqparse, fields, marshal

#from app.main.forms import RegisterForm, LoginForm,\
#    UserForm

#from werkzeug import check_password_hash, generate_password_hash

from werkzeug import secure_filename

from app import app, db, bcrypt, api
from app.main.models import User, Project, Project_image

from flask.ext.httpauth import HTTPBasicAuth

import datetime

#from flask.ext.admin import helpers


main = Blueprint('main', __name__, template_folder='../templates/main/')

auth = HTTPBasicAuth()


@main.route('/')
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@main.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"success": True})
    return 'file upload'


@auth.get_password
def get_password(username):
    if username == 'test':
        return 'test'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from
    # displaying the default auth dialog


@main.route('/user/<url>', methods=['GET'])
def user(url):
    user = User.query.filter_by(url=url).first()
    if user is None:
        return page_not_found(404)
    return render_template("user.html", user=user)


# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#     Login form
#     """
#     if current_user is not None and current_user.is_authenticated():
#         return redirect(url_for('main.home'))
#     form = LoginForm(request.form)
#     # make sure data are valid, but doesn't validate password is right
#     if request.method == 'POST' and form.validate():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
#             # the session can't be modified as it's signed,
#             # it's a safe place to store the user id
#             #session['user_id'] = user.id
#             login_user(user)
#             return redirect(request.args.get('next') or url_for('main.index'))
#         flash('Wrong email or password', 'error-message')
#     return render_template("login.html", form=form)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/login', methods=['GET', 'POST'])
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.index'))
    registerForm = RegisterForm(request.form, prefix="registerForm")
    loginForm = LoginForm(request.form, prefix="loginForm")

    # log in user
    if request.method == 'POST' and loginForm.validate():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd,
                                               loginForm.passwd.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            #session['user_id'] = user.id
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Wrong email or password', 'error-message')

    # register user
    if request.method == 'POST' and registerForm.validate():

        user = User(email=registerForm.email.data,
                    passwd=bcrypt.generate_password_hash(
                        registerForm.passwd.data),
                    name=registerForm.name.data)
        user.url = urllib.quote_plus(registerForm.name.data)
        #user_url = user_make_url(registerForm.name.data)
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('register.html',
                           registerForm=registerForm,
                           loginForm=loginForm)


@main.route("/logout/")
@login_required
def logout():
    logout_user()
    g.user = None
    flash("Logged out.")
    return redirect(url_for("main.index"))


@main.route('/user/<url>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(url):
    user = User.query.filter_by(url=url).first()
    if user is None:
        return page_not_found(404)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        g.user.name = form.name.data
        g.user.location = form.location.data
        g.user.url = urllib.quote_plus(form.name.data)
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('main.user', url=g.user.url))
    return render_template('user_manage.html',
                           form=form, user=user)


# Project Views
@main.route('/projects/<url>', methods=['GET'])
def projects(url):
    project = Project.query.filter_by(url=url).first()
    if project is None:
        return page_not_found(404)
    return render_template("project.html", project=project)


@main.route('/start', methods=('GET', 'POST'))
@login_required
def start():
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          need=form.need.data,
                          rewards=form.rewards.data)
        project.url = urllib.quote_plus(form.name.data)
        db.session.add(project)

        role = Role(role='owner', created_at=datetime.datetime.now())
        db.session.add(role)

        role.user = current_user
        role.project = project
        db.session.commit()

        return redirect(url_for('main.projects', url=project.url))

    return render_template('new_project.html', form=form)

# manage project

# @main.route('/projects/<projects>/manage', methods=['GET', 'POST'])
# @login_required
# def manage(projects):
#     project = User.query.filter_by(url=projects).first()
#     if project is None:
#         return page_not_found(404)
#     form = ProjectForm(obj=project)
#     if form.validate_on_submit():
#         g.project.name = form.name.data
#         g.project.status = form.status.data
#         g.project.description = form.description.data
#         g.project.need = form.need.data
#         g.project.rewards = form.rewards.data
#         g.project.url = urllib.quote_plus(form.name.data)
#         db.session.add(g.project)
#         db.session.commit()
#         return redirect(url_for('main.projects', name=g.project.name))
#     return render_template('',
#                            form=form, user=user)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Errors #
##########


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# @main.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500
