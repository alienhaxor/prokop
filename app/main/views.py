from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for

from flask.ext.login import login_user, logout_user,\
    current_user, login_required

from app.main.forms import LoginForm, RegistrationForm

#from app.main.forms import UserForm

#from werkzeug import check_password_hash, generate_password_hash

from app import db, bcrypt, lm
from app.main.models import User

#from flask.ext.admin import helpers


main = Blueprint('main', __name__, template_folder='../templates/main/')


@main.route('/')
def index():
    return 'hello2'


@main.route('/user/<int:id>', methods=['GET'])
def user(id):
    user = User.query.get(int(id))
    if user is None:
        return 'not_found'
    return render_template("user_profile.html", user=user)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main.user/%s' % g.user.name))
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            #session['user_email'] = user.email
            login_user(user)
            #flash('Welcome %s' % user.name)
            return redirect(url_for('main.user/%s' % g.user.name))
            #return redirect(request.args.get('next') or url_for('main.hi'))
        flash('Wrong email or password', 'error-message')
    return render_template("forms.html", form=form)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/register/', methods=('GET', 'POST'))
def register_view():
    form = RegistrationForm(request.form)
    if form.validate():

        user = User(email=form.email.data,
                    passwd=bcrypt.generate_password_hash(form.passwd.data),
                    name=form.name.data)

        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('forms.html', form=form)


@main.route("/logout/")
@login_required
def logout():
    logout_user()
    g.user = None
    flash("Logged out.")
    return redirect(url_for("main.index"))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
