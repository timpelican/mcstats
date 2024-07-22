from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    heroes = [
        {
            'name': 'Captain America',
            'aspect': 'Leadership'
        },
        {
            'name': 'Iron Man',
            'aspect': 'Aggression'
        }
    ]
    return render_template('index.html', heroes=heroes)
