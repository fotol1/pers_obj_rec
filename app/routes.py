from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, LikeForm
from app.models import User, Item, Score, Provider, Items_in_Provider, Interaction
from config import CINEMA_TO_SHOW, CURRENT_USER_FACTORS_PATH, flash_messages
from config import MOVIES_TO_SHOW
from recommenders.models import DumnRecommender, ALSRecommender
from app.utils import find_negative_item, find_similar_user
import numpy as np
from db_handler import DBHandler


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
# @login_required
def index():

    db_handler = DBHandler()
    all_providers = db_handler.get_all_providers()

    providers_selected = np.random.choice(
        all_providers, size=CINEMA_TO_SHOW, replace=False
    )

    is_auth = current_user.is_authenticated

    negative_item = None
    similar_user = None

    if is_auth:
        user_id = current_user.id
        negative_item = find_negative_item(user_id)
        similar_user = find_similar_user(user_id)

    feedback = LikeForm()

    if feedback.validate_on_submit():

        db_handler.add_interaction(user_id=user_id, item_id=negative_item.id)
        flash(flash_messages["got_feedback"])
        redirect(url_for("index"))

    return render_template(
        "index.html",
        providers=providers_selected,
        negative_item=negative_item,
        similar_user=similar_user,
        is_auth=is_auth,
        form=feedback,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    db_handler = DBHandler()

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()

    if form.validate_on_submit():
        user = db_handler.get_user_by_name(name=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash(flash_messages["invalid_login"])
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        flash(flash_messages["login_ok"])
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/cinema")
def cinema():

    db_handler = DBHandler()

    id = request.args.get("id")
    provider = db_handler.get_provider_by_id(id=id)

    movies_in = db_handler.get_items_in_provider(provider_id=provider.id)
    movies_id = [movie.id for movie in movies_in]
    movies_obj = db_handler.get_items_by_ids(movies_id)

    auth = current_user.is_authenticated
    """ We are going to sort movies for user """
    if auth:
        model = ALSRecommender()
        model.load()
        scores = model.score(id, movies_id)

        movies_obj = list(np.array(movies_obj)[np.argsort(scores)[::-1]])

    movies_obj = movies_obj[:MOVIES_TO_SHOW]

    return render_template(
        "cinema.html",
        provider=provider,
        movies=movies_obj,
        auth=auth,
        len_movies=len(movies_obj),
    )


@app.route("/logout")
def logout():
    flash(flash_messages["logout"])
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():

    db_handler = DBHandler()

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():

        db_handler.add_user(name=form.name.data, password=form.password.data)

        flash(flash_messages["new_user"])
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)
