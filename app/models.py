from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

saved_posts = db.Table(
    "saved_posts",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey('User.id'), primary_key=True),
    db.Column("course_id", db.ForeignKey('Course.id'), primary_key=True),
)

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    created_posts = db.relationship('Course', backref='User', lazy="dynamic")
    saved_posts = db.relationship('Course', secondary=saved_posts, back_populates="saved_by")

class Course(db.Model):
    __tablename__ = "Course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    content = db.Column(db.String(256))
    created_by = db.Column(db.Integer, db.ForeignKey('User.id'))
    saved_by = db.relationship('User', secondary=saved_posts, back_populates="saved_posts")

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User')


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
