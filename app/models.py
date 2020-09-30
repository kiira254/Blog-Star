from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, timezone, time, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String(255),unique=True,nullable=False)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash=db.Column(db.String(255))
    bio=db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    comment=db.relationship('Comment',backref='user',lazy='dynamic')
    blog=db.relationship('Blog',backref='user',lazy='dynamic')
    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot access the password')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.blog}')"

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id=db.Column(db.Integer,db.ForeignKey('blog.id'))


    def __repr__(self):
        return f"Comment ('{self.comment}','{self.user}')"
        
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog_id):
        comment=Comment.query.filter_by(blog_id=blog_id).all()
        return comment


class Blog(db.Model):
    __tablename__='blog'
    id=db.Column(db.Integer,primary_key=True)
    blog=db.Column(db.String())
    blog_category=db.Column(db.String(20))
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

class Quote:
    def __init__(self, id, author, quote, permalink):
        self.id = id
        self.author = author
        self.quote = quote
        self.permalink = permalink

