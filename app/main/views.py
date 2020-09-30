import os
import functools
import secrets
from flask import render_template,redirect,url_for,abort,flash,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Blog,Post
from .. import db,photos
from .forms import UpdateProfile,UploadBlog,CommentsForm
from flask import current_app
from ..requests import getQuotes

@main.route('/')
def index():

    title = 'bloges | Hub'
    quotes = getQuotes()
    posts = Post.query.all()
    return render_template('index.html', quotes=quotes, posts=posts, current_user=current_user)
    page=request.args.get('page',1,type=int)
    all_blog=blog.query.order_by(blog.posted.desc()).paginate(page=page,per_page=10)
  
    return render_template('index.html',bloges=all_blog, title = title)

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
    blog=Uploadblog()
    if current_user is None:
        abort(404)
    if blog.validate_on_submit():
        blog=blog(blog_category=blog.category.data,blog=blog.blog.data,user=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('blog Uploaded')
        return redirect(url_for('main.index'))
    return render_template('profile/update_blog.html',blog=blog,title='Create blog',legend='Create blog')

@main.route('/<int:pname>/comment',methods=['GET','POST'])
@login_required
def comment(pname):
    comment=CommentsForm()
    image=url_for('static',filename='profile/'+ current_user.profile_pic_path)
    blog=blog.query.filter_by(id=pname).first()
    comment_query=Comment.query.filter_by(blog_id=blog.id).all()
    
    if request.args.get('likes'):
        blog.upvotes=blog.upvotes+int(1)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    
    elif request.args.get('dislike'):
        blog.downvotes=blog.downvotes+int(1)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    if comments.validate_on_submit():
        comment=Comment(comment=comments.comment.data,blog_id=blog.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))
    
    return render_template('blog.html',comment=comments,blog=blog,comments=comment_query,title='blog Comment',image=image)

@main.route('/<int:pname>/update',methods=['GET','POST'])
@login_required
def update(pname):
    bloges=Uploadblog()
    blog=blog.query.get(pname)
    if blog.user != current_user:
        abort(403)
    if bloges.validate_on_submit():
        blog.blog_category=bloges.category.data
        blog.blog=bloges.blog.data
        db.session.commit()
        flash('Successfully Updated!')
        return redirect(url_for('main.profile',uname=blog.user.username))
    elif request.method=='GET':
        bloges.category.data=blog.blog_category
        bloges.blog.data=blog.blog

    return render_template('profile/update_blog.html',blog=bloges,legend="Update blog")

@main.route('/<int:blog_id>/delete',methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog=blog.query.get(blog_id)
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
    all_blog=blog.query.filter_by(user=user)\
            .order_by(blog.posted.desc())\
            .paginate(page=page,per_page=10)

    return render_template('posted_by.html',bloges=all_blog,title=user.username,user=user,image=image)

@main.route('/blog/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    blog_id = blog.query.filter_by(id=id).first()

    if blog_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, bloges_id=blog_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_blog', id=id))



@main.route('/blog/downvote/<int:id>')
@login_required
def downvote(id):
    blog_id = blog.query.filter_by(id=id).first()

    new_vote = Votes(vote=int(2), user_id=current_user.id, bloges_id=blog_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_blog', id=id))

@main.route('/blog/downvote/<int:id>')
@login_required
def vote_count(id):

    votes = Votes.query.filter_by(user_id=current_user.id).all()

    total_votes = votes.count()

    return total_votes

@main.route('/like/<int:blog_id>/<action>')
@login_required
def like_action(comment_id, action):
    comment = Comment.query.filter_by(id=post_id).first_or_404()
    if action == 'vote':
        current_user.vote_comment(comment)
        db.session.commit()
    if action == 'downvote':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(request.referrer) 