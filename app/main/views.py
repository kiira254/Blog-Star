from flask import render_template
from app import app

# views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')

@app.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
  title = 'Home - Welcome to The best Pitch Website'
    return render_template('index.html', title = title)