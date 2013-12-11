import os, json, urllib

from flask import Blueprint, request, render_template, flash,\
    g, redirect, url_for, jsonify, make_response, abort

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


@main.route('/projects/')
@main.route('/')
def index():
    projects = Project.query.all()
    return render_template("index.html", projects=projects)


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

#################
# User Views
#################


@main.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/user/<url>', methods=['GET'])
def user(url):
    user = User.query.filter_by(url=url).first()
    if user is None:
        return page_not_found(404)
    return render_template("user.html", user=user)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.index'))
    registerForm = RegisterForm(request.form, prefix="registerForm")
    loginForm = LoginForm(request.form, prefix="loginForm")

    # log in user
    if request.method == 'POST':
        if request.form['submit'] == 'login' \
                and loginForm.validate_on_submit():

            user = User.query.filter_by(email=loginForm.email.data).first()
            if user and bcrypt.check_password_hash(user.passwd,
                                                   loginForm.passwd.data):

                login_user(user)
                return redirect(request.args.get('next')
                                or url_for('main.index'))
            flash('Wrong email or password', 'error-message')

    return render_template('register.html',
                           form="login",
                           loginForm=loginForm,
                           registerForm=registerForm)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.index'))
    registerForm = RegisterForm(request.form, prefix="registerForm")
    loginForm = LoginForm(request.form, prefix="loginForm")

    if request.method == 'POST':
        if request.form['submit'] == 'register' and registerForm.validate():

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
            return redirect(request.args.get('next')
                            or url_for('main.index'))

    return render_template('register.html',
                           form="signup",
                           loginForm=loginForm,
                           registerForm=registerForm)


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
        g.user.description = form.description.data
        g.user.url = urllib.quote_plus(form.name.data)
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('main.user', url=g.user.url))
    return render_template('user_manage.html',
                           form=form, user=user)


#################
# Project Views
#################

@main.route('/projects/<url>', methods=['GET'])
def project(url):
    project = Project.query.filter_by(url=url).first()
    if project is None:
        return page_not_found(404)
    status_choices = dict(app.config['PROJECT_STATUS'])
    applied = False
    if current_user.is_authenticated():
        role = Role.query.filter_by(user=g.user)\
            .filter_by(project=project).first()
        if role:
            applied = True
    return render_template("project.html", project=project,
                           status_choices=status_choices, applied=applied)


# # Project Views
# @main.route('/projects/', methods=['GET'])
# def projects(url):
#     projects = Project.query.all()
#     return render_template("project.html", project=project)


@main.route('/start', methods=('GET', 'POST'))
@login_required
def start():
    form = ProjectForm(request.form)
    form.status.data = '1'
    if request.method == 'POST' and form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          need=form.need.data,
                          rewards=form.rewards.data,
                          status='1',
                          video_url=form.video_url.data,
                          image_url=form.image_url.data
                          )
        project.url = urllib.quote_plus(form.name.data)
        db.session.add(project)

        role = Role(role='owner', created_at=datetime.datetime.now())
        db.session.add(role)

        role.user = current_user
        role.project = project
        db.session.commit()

        return redirect(url_for('main.project', url=project.url))

    return render_template('new_project.html', form=form)


#manage project
@main.route('/projects/<project>/manage', methods=['GET', 'POST'])
@login_required
def project_manage(project):
    project = Project.query.filter_by(url=project).first()
    for role in project.roles:
        if role.role == 'owner':
            if g.user.id is not role.user.id:
                # TODO: replace with 'not_authorized'
                return page_not_found(404)

    if project is None:
        return page_not_found(404)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          status=form.status.data,
                          description=form.description.data,
                          need=form.need.data,
                          rewards=form.rewards.data,
                          url=urllib.quote_plus(form.name.data)
                          )

        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.project', url=project.url))

    return render_template('project_manage.html',
                           form=form, project=project)


#Sign up for project
@main.route('/project/signup/<project_url>/<user_url>/<role>',
            methods=['GET', 'POST'])
@login_required
def project_signup(project_url, user_url, role):
    project = Project.query.filter_by(url=project_url).first()
    if not project:
        abort(404)
    user = User.query.filter_by(url=user_url).first()
    if not user:
        abort(404)

    userRole = Role.query.filter_by(user=user)\
        .filter_by(project=project).first()
    if userRole:
        userRole.role = role
    else:
        userRole = Role(role=role, created_at=datetime.datetime.now())
        userRole.user = current_user
        userRole.project = project
        db.session.add(userRole)

    db.session.commit()
    return 'success', 201

# Errors #
##########


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# @main.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500
