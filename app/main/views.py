import os, json

from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for, jsonify, abort, make_response

from flask.ext.login import login_user, logout_user,\
    current_user, login_required

from app.main.forms import LoginForm, RegistrationForm

from flask.ext.restful import Resource, reqparse, fields, marshal

#from app.main.forms import RegisterForm, LoginForm,\
#    UserForm

#from werkzeug import check_password_hash, generate_password_hash

from werkzeug import secure_filename

from app import app, db, bcrypt, api
from app.main.models import User, Project, Project_image

from flask.ext.httpauth import HTTPBasicAuth

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


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.home'))
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            #session['user_id'] = user.id
            login_user(user)
            flash('Welcome %s' % user.name)
            return redirect(request.args.get('next') or url_for('main.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("user/login.html", form=form)


@main.route('/register/', methods=['GET', 'POST'])
def register_view():
    form = RegistrationForm(request.form)
    if form.validate_form_on_submit(form):

        user = User(name=form.name.data, email=form.email.data,
                    password=bcrypt.generate_password_hash(form.password.data))

        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        login.login_user(user)
        return redirect(url_for('index'))

    return render_template('form.html', form=form)


@main.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("main.index"))
