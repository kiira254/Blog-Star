from flask import render_template
from app import app

# views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')

@app.route('/blog/<int:blog_id>')
def blog(blog_id):

    '''
    View blog page function that returns the blog details page and its data
    '''
  title = 'Home - Welcome to The best blog Website'
    return render_template('index.html', title = title)