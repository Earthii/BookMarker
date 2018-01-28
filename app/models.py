from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
# to create a new bookmark : db.session.add(Bookmark(url,date,description))
# The db is like a unit of work
# to commit : db.session.commit()
# To query : Bookmark.query.get(primary_key), Bookmark.query.all()
# To query specific rows : Bookmark.query.filter_by(username="earthii").first()

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    # link with user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        # return a limited number of most recent
        return Bookmark.query.order_by(Bookmark.date.desc()).limit(num)

    # enable clear printing
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


# import UserMixin for login feature
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    # link with bookmark table
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    """
        password_hash contains the hash of the password. 
        It is a write only field. So we can set the value as a String
        but only read it as a hash.
    """
    password_hash = db.Column(db.String)

    # raise error if we try to read it directly
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    # generate a password hash and set it into the password_hash attribute
    # when ever attribute password is given
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # check a string against the hash when a user logs in
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' %self.username

