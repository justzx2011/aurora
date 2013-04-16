from aurora_app.constants import ROLES
from aurora_app.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(160))
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=ROLES['USER'])

    def __init__(self, username, password, email=None, role=None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(128), nullable=True)
    vcs_url = db.Column(db.String(128), nullable=True)
    vcs_type = db.Column(db.SmallInteger, nullable=True)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)


class Stage(db.Model):
    __tablename__ = "stages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    branch = db.Column(db.String(32), nullable=True)

    def __init__(self, *args, **kwargs):
        super(Stage, self).__init__(*args, **kwargs)


class Host(db.Model):
    __tablename__ = "hosts"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column