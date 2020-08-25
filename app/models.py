from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    latest_login = db.Column(db.DateTime, default=datetime.now)
    point = db.Column(db.Integer, default=0, nullable=True)
    level = db.Column(db.Integer, default=1, nullable=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    likes = db.relationship("Like", backref="like", lazy="dynamic")

    def __init_(self, point, level):
        self.point = 0
        self.level = 1

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    content = db.Column(db.String(280))
    posted_at = db.Column(db.DateTime, index=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)
    receiver = db.Column(db.String(64))
    anonymous = db.Column(db.Boolean, default=False)
    sender = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    likes = db.relationship("Like", backref="user_like", lazy="dynamic")

    def __repr__(self):
        return "<Post {}>".format(self.content)

    def updated_at(self):
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit(self)


class Like(db.Model):
    user = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
