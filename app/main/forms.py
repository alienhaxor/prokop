from flask.ext.wtf import Form

from wtforms import TextField, BooleanField, TextAreaField,\
    RadioField, PasswordField, DecimalField

from wtforms.validators import Required, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.main.models import User

from wtforms_alchemy import ModelForm


class LoginForm(Form):
    email = TextField('Email address', [Required(), Email()])
    passwd = PasswordField('Password', [Required()])


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
