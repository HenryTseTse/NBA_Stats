from flask import redirect, render_template, request, flash, session, g
from sqlalchemy.exc import IntegrityError

from models import db, User
from forms import SignupForm, LoginForm, PlayerForm, AdvancedForm, TeamsForm
from service.nba_api import (
    search_player,
    search_player_adv,
    search_games,
    search_teams,
    PlayerStats,
)
from dal.database import signup, get_leader_stats
from readcsv import get_player_image

CURR_USER_KEY = "curr_user"


def before_request():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def after_request(req):
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers["Cache-Control"] = "public, max-age=0"
    return req


def homepage():
    result = get_leader_stats()
    if g.user:
        return render_template(
            "search_home.html",
            scoring_leaders=result["scoring_leaders"],
            rebounding_leaders=result["rebounding_leaders"],
            assisting_leaders=result["assisting_leaders"],
            stealing_leaders=result["stealing_leaders"],
            blocking_leaders=result["blocking_leaders"],
        )
    else:
        return render_template(
            "home.html",
            scoring_leaders=result["scoring_leaders"],
            rebounding_leaders=result["rebounding_leaders"],
            assisting_leaders=result["assisting_leaders"],
            stealing_leaders=result["stealing_leaders"],
            blocking_leaders=result["blocking_leaders"],
        )


def do_login(user):
    """Handle user login."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Handle logout of user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = signup(
                username=form.username.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)

        do_login(user)
        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)


def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("users/login.html", form=form)


def logout():
    do_logout()
    flash("Succuessfully logged out!", "success")
    return redirect("/")


def get_player_stats():
    form = PlayerForm()
    if form.validate_on_submit():
        player_image = get_player_image(
            str(form.first_name.data), str(form.last_name.data)
        )
        player_full_name = form.first_name.data + " " + form.last_name.data
        results = search_player(player_full_name)

        if results is None:
            flash("Player not found", "danger")
            return redirect("/api/player-stats")
        else:
            return render_template(
                "players/stat.html",
                results=results,
                name=player_full_name.title(),
                image=player_image,
            )

    else:
        return render_template("players/career_stat_search.html", form=form)


def get_adv_player_stats():
    form = AdvancedForm()
    if form.validate_on_submit():
        player_image = get_player_image(
            str(form.first_name.data), str(form.last_name.data)
        )
        player_full_name = form.first_name.data + " " + form.last_name.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        pts = form.pts.data or 0
        reb = form.reb.data or 0
        ast = form.ast.data or 0
        stl = form.stl.data or 0
        blk = form.blk.data or 0
        playerstats = PlayerStats(pts, reb, ast, stl, blk)
        results = search_player_adv(player_full_name, start_date, end_date, playerstats)

        if results is None:
            flash("Player not found", "danger")
            return redirect("/api/adv-player-stats")
        else:
            return render_template(
                "players/adv_stat.html",
                results=results,
                name=player_full_name.title(),
                image=player_image,
            )

    else:
        return render_template("players/adv_stat_search.html", form=form)


def get_teams():
    results = search_teams()
    return render_template("teams/all_teams.html", results=results)


def get_h2h_stats():
    form = TeamsForm()
    if form.validate_on_submit():
        team = form.team.data
        season = form.season.data
        postseason = form.postseason.data
        results = search_games(team, season, postseason)

        if results is None:
            flash("Season not found", "danger")
            return redirect("/api/head-to-head")
        else:
            return render_template("teams/team_stats.html", results=results)
    else:
        return render_template("teams/team_search.html", form=form)
