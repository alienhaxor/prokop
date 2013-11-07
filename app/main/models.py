from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    email = db.Column(db.String(90), index=True)
    passwd = db.Column(db.String(512))
    date_created = db.Column(db.DateTime)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __init__(self, name=None, url=None, email=None,
                 passwd=None, about=None, city=None,
                 lastSeen=None, date_created=None, avatar=None):
        self.name = name
        self.url = url
        self.email = email
        self.passwd = passwd
        self.date_created = datetime.datetime.now()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': dump_datetime(self.date_created)
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    student_points = db.Column(db.Integer)
    info = db.Column(db.String(5012))
    picture_url = db.Column(db.String)
    active = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)

    #users = db.relationship('Project', backref='project_role')

    def __init__(self, name=None, url=None, student_points=None,
                 info=None, picture_url=None, active=None,
                 date_created=None):
        self.name = name
        self.url = url
        self.student_points = student_points
        self.info = info
        self.picture_url = picture_url
        self.active = active
        self.date_created = datetime.datetime.now()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': dump_datetime(self.date_created)
        }


class Role(db.Model):
    #__tablename__ == 'role'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        primary_key=True)
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id'),
                           primary_key=True)
    role = db.Column(db.String(64))
    team = db.Column(db.String(64))
    created_at = db.Column(db.DateTime)
    token = db.relationship("User", backref="project_role")
    #game = db.relationship("Game", backref="token_assocs")


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
