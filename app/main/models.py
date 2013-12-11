from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    email = db.Column(db.String(90), index=True)
    passwd = db.Column(db.String(512))
    description = db.Column(db.String(2046))
    location = db.Column(db.String(64))
    date_created = db.Column(db.DateTime)
    projects = db.relationship('Role', backref='project_role')

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def check_unique_email(email):
        if User.query.filter_by(email=email).first() is not None:
            return True
        else:
            return False

    @staticmethod
    def check_unique_name(name):
        if User.query.filter_by(name=name).first() is not None:
            return True
        else:
            return False

    @staticmethod
    def check_unique_url(url):
        if User.query.filter_by(url=url).first() is not None:
            return True
        else:
            return False

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
    description = db.Column(db.String(2056))
    need = db.Column(db.String(2056))
    rewards = db.Column(db.String(512))
    status = db.Column(db.String(64), default='1')
    video_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    need_leader = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime)
    images = db.relationship('Project_image', backref='project',
                             lazy='dynamic')
    roles = db.relationship('Role', backref='project_assocs')

    #users = db.relationship('Project', backref='project_role')

    def __init__(self, name=None, url=None, student_points=None,
                 description=None, image_url=None, video_url=None,
                 status=None, date_created=None, need=None,
                 rewards=None, need_leader=None):
        self.name = name
        self.url = url
        self.student_points = student_points
        self.description = description
        self.image_url = image_url
        self.video_url = video_url
        self.status = status
        self.date_created = datetime.datetime.now()
        self.need = need
        self.rewards = rewards
        self.need_leader = need_leader

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture_url': self.picture_url,
            'releaseDate': dump_datetime(self.date_created),
            'images': self.serialize_many2many
        }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [project_image.serialize for project_image in self.images]

    @staticmethod
    def check_unique_proj_name(name):
        if Project.query.filter_by(name=name).first() is not None:
            return True
        else:
            return False

    @staticmethod
    def check_unique_proj_url(url):
        if Project.query.filter_by(url=url).first() is not None:
            return True
        else:
            return False


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
    user = db.relationship("User", backref="project_role")
    project = db.relationship("Project", backref="project_assocs")


class Project_image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), index=True)
    cover = db.Column(db.Boolean(), default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'url': self.url,
            'cover': self.cover
        }


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
