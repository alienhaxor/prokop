from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from config import basedir
import redis

from flask import render_template

app = Flask(__name__)
#red = redis.Redis("localhost")

app.debug = True

# sqlalchemy, migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'main.login'
lm.logout_view = 'main.logout'
lm.login_message = u"Please log in to access this page."

# File Uploads
#UPLOAD_FOLDER = os.path.join(basedir, '')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

toolbar = DebugToolbarExtension(app)

from app.main import models, views
from app.main.views import main

app.register_blueprint(main, url_prefix='')

# Errors #
##########


@app.errorhandler(404)
def not_found(error):
    return render_template('/error/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('/error/500.html'), 500
