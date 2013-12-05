from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, TextAreaField,\
    RadioField, PasswordField, DecimalField, form, fields, validators

from wtforms.validators import Required, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.main.models import User, Project

#from wtforms_alchemy import ModelForm
from app import bcrypt


class LoginForm(Form):
    email = fields.TextField('Email address', [Required(), Email()])
    passwd = fields.PasswordField('Password', [Required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid email or password')

        if not bcrypt.check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid email or password')

    def get_user(self):
        return User.query.filter_by(email=self.email.data).first()


class RegisterForm(Form):
    email = fields.TextField('Email address', [Required()])
    passwd = fields.PasswordField('Password', [Required()])
    name = fields.TextField('Name', [Required()])

    def validate_login(self, field):
        if (User.query.filter_by(url=self.url.data).first()):
            raise validators.ValidationError('Duplicate username')


# edit user.
class UserForm(Form):
    name = TextField('name', [Required()])
    url = TextField('name')
    email = TextField('email')
    location = TextField('location')
    description = TextAreaField('description',
                                validators=[Length(min=0, max=140)])
    passwd_old = fields.PasswordField('old password')
    passwd_new = fields.PasswordField('new password')

    # def __init__(self, original_url, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #     self.original_url = original_url

    # def validate(self):
    #     if not Form.validate(self):
    #         return False
    #     if self.url.data == self.original_url:
    #         return True
    #     user_url = User.query.filter_by(url=self.url.data).first()
    #     if user_url is not None:
    #         self.url.errors.append(
    #             'This url is already in use. Please choose another one.'
    #         )
    #         return False
    #     return True


class ProjectForm(Form):
    name = TextField('name')
    status = TextField('status')
    description = TextAreaField('description')
    need = TextAreaField('need')
    rewards = TextAreaField('rewards')
    student_points = TextField('student_points')
    picture = TextField('textfield')

    # def __init__(self, original_url, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #     self.original_url = original_url

    # def validate(self):
    #     if not Form.validate(self):
    #         return False
    #     if self.url.data == self.original_url:
    #         return True
    #     project_url = Project.query.filter_by(url=self.url.data).first()
    #     if project_url is not None:
    #         self.url.errors.append(
    #             'This url is already in use. Please choose another one.'
    #         )
    #         return False
    #     return True
