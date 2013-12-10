from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, TextAreaField,\
    RadioField, SelectField, PasswordField, DecimalField, form, fields, validators

from wtforms.validators import Required, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.main.models import User, Project

#from wtforms_alchemy import ModelForm
from app import bcrypt, app


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
                                validators=[Length(min=0, max=2056)])
    passwd_old = fields.PasswordField('old password')
    passwd_new = fields.PasswordField('new password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user_url = User.query.filter_by(url=self.url.data).first()
        if user_url:
            self.url.errors.append(
                'This url is already in use. Please choose another one.'
            )
            return False
        else:
            return True


class ProjectForm(Form):
    name = TextField('Name')
    #url = TextField('name')
    status = SelectField("Status", coerce=str,
                         choices=app.config['PROJECT_STATUS'])

    description = TextAreaField('Description')
    need = TextAreaField('Need')
    rewards = TextAreaField('Rewards')
    student_points = TextField('Student points')
    picture = TextField('textfield')

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)

    # def validate(self):
    #     if not Form.validate(self):
    #         return False

        # project_url = Project.query.filter_by(url=self.name.data).first()
        # if project_url:
        #     self.url.errors.append(
        #         'This url is already in use. Please choose another one.'
        #     )
        #     return False
        # else:
        #     return True
