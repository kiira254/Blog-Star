import os
import functools
import secrets
from flask import render_template,redirect,url_for,abort,flash,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Blog
from .. import db,photos
from .forms import UpdateProfile,UploadBlog,CommentsForm
from flask import current_app
from ..requests import get_quotes

@main.route('/')
def index():
    quotes = get_quotes()
    title = 'Blogs | Hub'
    page=request.args.get('page',1,type=int)
    all_blog=Blog.query.order_by(Blog.posted.desc()).paginate(page=page,per_page=10)
  
    return render_template('index.html',blogs=all_blog, title = title, quotes=quotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
   
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/upload/blog',methods=['GET','POST'])
@login_required
def upload_blog():
    blog=UploadBlog()
    if current_user is None:
        abort(404)
    if blog.validate_on_submit():
        blog=Blog(blog=blog.blog.data,user=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Blog Uploaded')
        return redirect(url_for('main.index'))
    return render_template('profile/update_blog.html',blog=blog,title='Create Blog',legend='Create Blog')

@main.route('/<int:pname>/update',methods=['GET','POST'])
@login_required
def update(pname):
    blogs=UploadBlog()
    blog=Blog.query.get(pname)
    if blog.user != current_user:
        abort(403)
    if blogs.validate_on_submit():
        blog.blog_category=blogs.category.data
        blog.blog=blogs.blog.data
        db.session.commit()
        flash('Successfully Updated!')
        return redirect(url_for('main.profile',uname=blog.user.username))
    elif request.method=='GET':
        blogs.category.data=blog.blog_category
        blogs.blog.data=blog.blog

    return render_template('profile/update_blog.html',blog=blogs,legend="Update Blog")

@main.route('/<int:blog_id>/delete',methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog=Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.profile',uname=blog.user.username))


@main.route('/profile/user/<string:username>')
def posted(username):
    user=User.query.filter_by(username=username).first_or_404()
    image=url_for('static',filename='profile/'+ user.profile_pic_path)
    page=request.args.get('page',1,type=int)
    all_blog=Blog.query.filter_by(user=user)\
            .order_by(Blog.posted.desc())\
            .paginate(page=page,per_page=10)

    return render_template('posted_by.html',blogs=all_blog,title=user.username,user=user,image=image)

   