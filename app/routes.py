from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, VillainForm, HeroForm
from app.models import Phase, Aspect

@app.route('/')
@app.route('/index')
def index():
    phases = Phase.query.order_by('id').all()
    return render_template('index.html', phases=phases)

@app.route('/stats')
def stats():
    phases = Phase.query.order_by('id').all()
    return render_template('stats.html', phases=phases)

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
    #TODO: Need an actual error when no Phases are defined.
    # Currently generates an unsubmittable form.
    form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
    if form.validate_on_submit():
        flash('New villain {}, from phase {}'.format(
            form.name.data, form.phase.data))
        return redirect(url_for('index'))
    return render_template('villain.html', title='Villain', form=form)

@app.route('/hero', methods=['GET', 'POST'])
def hero():
    form = HeroForm()
    #TODO: Need an actual error when no Phases are defined.
    # Currently generates an unsubmittable form.
    form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
    #TODO: Ditto for Aspects.
    form.aspect.choices = [(a.id, a.name) for a in Aspect.query.order_by('id')]
    if form.validate_on_submit():
        flash('New hero {}, from phase {} with default aspect {}'.format(
            form.name.data, form.phase.data, form.aspect.data))
        return redirect(url_for('index'))
    return render_template('hero.html', title='Hero', form=form)