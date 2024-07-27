from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, VillainForm, HeroForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/villain', methods=['GET', 'POST'])
def villain():
    form = VillainForm()
    if form.validate_on_submit():
        flash('New villain {}, from phase {}'.format(
            form.name.data, form.phase.data))
        return redirect(url_for('index'))
    return render_template('villain.html', title='Villain', form=form)

@app.route('/hero', methods=['GET', 'POST'])
def hero():
    form = HeroForm()
    if form.validate_on_submit():
        flash('New hero {}, from phase {} with default aspect {}'.format(
            form.name.data, form.phase.data, form.aspect.data))
        return redirect(url_for('index'))
    return render_template('hero.html', title='Hero', form=form)