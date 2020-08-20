from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    # likes = db.relationship("Like", backref="like", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280))
    posted_at = db.Column(db.DateTime, index=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    # likes = db.relationship(
    #     "Like", secondary=post_like, backref="user_like", lazy="dynamic"

    def __repr__(self):
        return "<Post {}>".format(self.content)


class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)


# Like = db.Table(
#     "post_like",
#     db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True),
#     db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
# )
