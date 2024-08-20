from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, VillainForm, HeroForm
from app.models import Phase, Aspect, User, Result
from urllib.parse import urlsplit


@app.route('/')
@app.route('/index')
def index():
    phases = Phase.query.order_by('id').all()
    return render_template('index.html', phases=phases)

@app.route('/stats')
def stats():
    phases = Phase.query.order_by('id').all()
    #TODO: this could get inefficient with lots of results
    results = Result.query.order_by('id').all()
    return render_template('stats.html', phases=phases, results=results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/villain', methods=['GET', 'POST'])
@login_required
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
@login_required
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

@app.route('/forcederror', methods=['GET'])
def forcederror():
    a = Aspect()
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('index'))