from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, TextAreaField,\
    RadioField, PasswordField, DecimalField, form, fields, validators

from wtforms.validators import Required, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.main.models import User, Project

#from wtforms_alchemy import ModelForm
from app import bcrypt


class LoginForm(form.Form):
    email = fields.TextField(validators=[validators.required()])
    passwd = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid email or password')

        if not bcrypt.check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid email or password')

    def get_user(self):
        return User.query.filter_by(email=self.email.data).first()


class RegistrationForm(form.Form):
    email = fields.TextField(validators=[validators.required()])
    passwd = fields.PasswordField(validators=[validators.required()])
    name = fields.TextField(validators=[validators.required()])

    def validate_login(self, field):
        if (User.query.filter_by(url=self.url.data).first()):
            raise validators.ValidationError('Duplicate username')


# edit user.
class UserForm(Form):
    name = TextField('name', validators=[
        Length(min=1, max=64),
        Required()])
    url = TextField('url', validators=[
        Length(min=1, max=64),
        Required()])
    email = TextField('email', validators=[
        Length(min=6, max=90),
        Required()])

    def __init__(self, original_url, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_url = original_url

    def validate(self):
        if not Form.validate(self):
            return False
        if self.url.data == self.original_url:
            return True
        user_url = User.query.filter_by(url=self.url.data).first()
        if user_url is not None:
            self.url.errors.append(
                'This url is already in use. Please choose another one.'
            )
            return False
        return True


class ProjectForm(Form):
    name = TextField('name', validators=[
        Length(min=1, max=64),
        Required()])
    url = TextField('url', validators=[
        Length(min=1, max=64),
        Required()])
    student_points = TextField('student_points')
    info = TextField('info', validators=[Length(min=1, max=5012), Required()])
    picture = TextField('textfield')

    def __init__(self, original_url, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_url = original_url

    def validate(self):
        if not Form.validate(self):
            return False
        if self.url.data == self.original_url:
            return True
        project_url = Project.query.filter_by(url=self.url.data).first()
        if project_url is not None:
            self.url.errors.append(
                'This url is already in use. Please choose another one.'
            )
            return False
        return True


class EditForm(Form):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required()])
    location = TextField('location', validators=[Required()])
    description = TextAreaField('description',
                                validators=[Length(min=0, max=140)])
    passwd_old = fields.PasswordField('old password',
                                      validators=[validators.required()])
    passwd_new = fields.PasswordField('new password',
                                      validators=[validators.required()])
