from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Item, Score, Provider, Items_in_Provider, Interaction
from config import CINEMA_TO_SHOW
from recommenders.models import DumnRecommender, ALSRecommender

import numpy as np


@app.route('/')
@app.route('/index')
# @login_required
def index():
    all_providers = Provider.query.all()
    providers_selected = np.random.choice(all_providers,
                                          size=CINEMA_TO_SHOW,
                                          replace=False)

    is_auth = current_user.is_authenticated

    items = Item.query.all()
    items_names = [item.name for item in items]
    items_ids = [item.id for item in items]

    similar_users = ['fff']

    if is_auth:
        user_id = current_user.id
        interacted_items = Interaction.query.filter_by(user_id=user_id).all()
        interacted_items_id = [item.item_id for item in interacted_items]
        not_interacted_items_id = list(set(items_ids) - set(interacted_items_id))
        not_interacted_items_names = Item.query.filter(Item.id.in_(not_interacted_items_id))
        not_interacted_items_names = not_interacted_items_names.all()
        not_interacted_items_name = np.random.choice(not_interacted_items_names)

    items_id = {(key, value) for key, value in zip(items_ids, items_names)}
    return render_template('index.html',
                           providers=providers_selected,
                           not_interacted_items_name=not_interacted_items_name,
                           similar_users=similar_users,
                           is_auth=is_auth)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/cinema')
def cinema():
    id = request.args.get('id')
    provider = Provider.query.filter_by(id=id).first()

    movies_in = Items_in_Provider.query.filter_by(provider_id=provider.id).all()
    movies_id = [movie.id for movie in movies_in]
    movies_obj = Item.query.filter(Item.id.in_(movies_id)).all()

    auth = current_user.is_authenticated
    """ We are going to sort movies for user """
    if auth:
        model = ALSRecommender()
        model.load()
        scores = model.score(id, movies_id)

        movies_obj = list(np.array(movies_obj)[np.argsort(scores)[::-1]])

    return render_template('cinema.html',
                           provider=provider,
                           movies=movies_obj,
                           auth=auth)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
