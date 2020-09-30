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
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")
    comments=db.relationship('Comment',backref='user',lazy='dynamic')
    blog=db.relationship('blog',backref='user',lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.blog}')"

class Blog(db.Model):
    __tablename__='blog'
    id=db.Column(db.Integer,primary_key=True)
    blog=db.Column(db.String())
    blog_category=db.Column(db.String(20))
    posted=db.Column(db.DateTime,default=timezone)
    upvotes=db.Column(db.Integer)
    downvotes=db.Column(db.Integer)
    comment=db.relationship('Comment',backref='blog',lazy='dynamic')
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class Clap(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def upvote(cls, id):
        upvote_post = Clap(user=current_user, post_id=id)
        upvote_post.save()

    @classmethod
    def query_upvotes(cls, id):
        upvote = Clap.query.filter_by(post_id=id).all()
        return upvote

    @classmethod
    def all_upvotes(cls):
        upvotes = Clap.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.post_id}'

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Post title: {self.title}, Date Posted: {self.date_posted}, Post Content: {self.content}'

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



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Review:


    all_reviews = []

    def __init__(self,title,imageurl,review):
        self.title = title
        self.imageurl = imageurl
        self.review = review


    def save_review(self):
        Review.all_reviews.append(self)


    @classmethod
    def clear_reviews(cls):
        Review.all_reviews.clear()

    @classmethod

    def get_reviews(cls,id):

        response = []

        for review in cls.all_reviews:
            if review.blog_id == id:
                response.append(review)

        return response

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    blog_review = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()
        return reviews