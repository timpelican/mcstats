from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, VillainForm, VillainDeleteForm, HeroForm, HeroDeleteForm
from app.models import Phase, Aspect, User, Result, Villain, Hero
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

@app.route('/villain/create', methods=['GET', 'POST'])
@login_required
def villain_create():
    form = VillainForm()
    #TODO: Need an actual error when no Phases are defined.
    # Currently generates an unsubmittable form.
    form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
    if form.validate_on_submit():
        v = Villain(name=form.name.data, phase_id=form.phase.data)
        db.session.add(v)
        db.session.commit()
        flash('New villain {}, from phase {}, created'.format(
            form.name.data, form.phase.data))
        return redirect(url_for('villain'))
    return render_template('villain.html', form=form)

@app.route('/villain')
def villain():
    villains=Villain.query.order_by('phase_id').all()
    return render_template('villain_list.html',villains=villains)

@app.route('/villain/<int:villain_id>')
def single_villain(villain_id):
    v = Villain.query.filter_by(id=villain_id).first()
    if v:
        return render_template('single_villain.html', villain=v)
    flash(f'Villain with id {villain_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/villain/<int:villain_id>/update', methods=['GET', 'POST'])
@login_required
def villain_update(villain_id):
    v = Villain.query.filter_by(id=villain_id).first()
    if v:
        form = VillainForm()
        #TODO: Need an actual error when no Phases are defined.
        # Currently generates an unsubmittable form.
        form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
        if form.validate_on_submit():
            v.name = form.name.data
            v.phase_id = form.phase.data
            db.session.commit()
            flash(f'Updated details for Villain {v.name}')
            return redirect(url_for('villain'))
        elif request.method == 'GET':
            form.name.data = v.name
            form.phase.data = v.phase_id
        return render_template('villain.html', title='Villain', form=form)
    flash(f'Villain with id {villain_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/villain/<int:villain_id>/delete', methods=['GET', 'POST'])
@login_required
def villain_delete(villain_id):
    v = Villain.query.filter_by(id=villain_id).first()
    if v:
        form = VillainDeleteForm()
        if form.validate_on_submit():
            db.session.delete(v)
            db.session.commit()
            flash(f'Deleted Villain {v.name}')
            return redirect(url_for('villain'))
        elif request.method == 'GET':
            pass
            # No fields to populate in the form
        return render_template('villain_delete.html', title='Villain', form=form, villain=v)
    flash(f'Villain with id {villain_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/hero/create', methods=['GET', 'POST'])
@login_required
def hero_create():
    form = HeroForm()
    #TODO: Need an actual error when no Phases are defined.
    # Currently generates an unsubmittable form.
    form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
    #TODO: Ditto for Aspects.
    form.aspect.choices = [(a.id, a.name) for a in Aspect.query.order_by('id')]
    if form.validate_on_submit():
        h = Hero(name=form.name.data, phase_id=form.phase.data, aspect_id=form.aspect.data)
        db.session.add(h)
        db.session.commit()
        flash('New hero {}, from phase {} with default aspect {}'.format(
            form.name.data, form.phase.data, form.aspect.data))
        return redirect(url_for('hero'))
    return render_template('hero.html', form=form)

@app.route('/hero')
def hero():
    heroes=Hero.query.order_by('phase_id').all()
    return render_template('hero_list.html',heroes=heroes)

@app.route('/hero/<int:hero_id>')
def single_hero(hero_id):
    h = Hero.query.filter_by(id=hero_id).first()
    if h:
        return render_template('single_hero.html', hero=h)
    flash(f'Hero with id {hero_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/hero/<int:hero_id>/update', methods=['GET', 'POST'])
@login_required
def hero_update(hero_id):
    h = Hero.query.filter_by(id=hero_id).first()
    if h:
        form = HeroForm()
        #TODO: Need an actual error when no Phases are defined.
        # Currently generates an unsubmittable form.
        form.phase.choices = [(p.id, p.phasename) for p in Phase.query.order_by('id')]
        #TODO: Ditto for Aspects.
        form.aspect.choices = [(a.id, a.name) for a in Aspect.query.order_by('id')]
        if form.validate_on_submit():
            h.name = form.name.data
            h.phase_id = form.phase.data
            h.aspect_id = form.aspect.data
            db.session.commit()
            flash(f'Updated details for Hero {h.name}')
            return redirect(url_for('hero'))
        elif request.method == 'GET':
            form.name.data = h.name
            form.phase.data = h.phase_id
            form.aspect.data = h.aspect_id
        return render_template('hero.html', title='Hero', form=form)
    flash(f'Hero with id {hero_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/hero/<int:hero_id>/delete', methods=['GET', 'POST'])
@login_required
def hero_delete(hero_id):
    h = Hero.query.filter_by(id=hero_id).first()
    if h:
        form = HeroDeleteForm()
        if form.validate_on_submit():
            db.session.delete(h)
            db.session.commit()
            flash(f'Deleted Hero {h.name}')
            return redirect(url_for('hero'))
        elif request.method == 'GET':
            pass
            # No fields to populate in the form
        return render_template('hero_delete.html', title='Hero', form=form, hero=h)
    flash(f'Hero with id {hero_id} does not exist!')
    return redirect(url_for('index'))

@app.route('/forcederror', methods=['GET'])
def forcederror():
    a = Aspect()
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('index'))
