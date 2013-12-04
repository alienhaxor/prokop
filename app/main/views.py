import os, json, urllib

from flask import Blueprint, request, render_template, flash,\
    g, redirect, url_for, jsonify, make_response

from flask.ext.login import login_user, logout_user,\
    current_user, login_required

from app.main.forms import LoginForm, RegisterForm, EditForm

from app import db, bcrypt, lm
from app.main.models import User

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


@main.route('/user/<name>', methods=['GET'])
def user(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        return page_not_found(404)
    return render_template("user.html", user=user)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.home'))
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            #session['user_id'] = user.id
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Wrong email or password', 'error-message')
    return render_template("forms.html", form=form)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    print 'JESUS'
    if form.validate_on_submit():
    	print 'JESUS HITLER'
        user = User(email=form.email.data,
                    passwd=bcrypt.generate_password_hash(form.passwd.data),
                    name=form.name.data)
        # user.url = urllib.urlencode(form.urlname.data)
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@main.route("/logout/")
@login_required
def logout():
    logout_user()
    g.user = None
    flash("Logged out.")
    return redirect(url_for("main.index"))


@main.route('/user/<name>/edit', methods=['GET', 'POST'])
@login_required
def edit(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        return page_not_found(404)
    form = EditForm(obj=user)
    if form.validate_on_submit():
        g.user.name = form.name.data
        g.user.url = urllib.quote_plus(form.name.data)
        #g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('main.user', name=g.user.name))
    return render_template('user_manage.html',
                           form=form, user=user)


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
