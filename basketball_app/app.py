import os

from flask import Flask

from dal.database import connect_db
from functions import (
    before_request,
    after_request,
    user_signup,
    homepage,
    login,
    logout,
    get_player_stats,
    get_adv_player_stats,
    get_teams,
    get_h2h_stats,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///nba-users"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret")

connect_db(app)


@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""
    before_request()


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""
    return after_request(req)


##############################################################################
# General user routes:


app.add_url_rule("/", "homepage", homepage)

app.add_url_rule("/signup", "user_signup", user_signup, methods=["GET", "POST"])

app.add_url_rule("/login", "login", login, methods=["GET", "POST"])

app.add_url_rule("/logout", "logout", logout)


##############################################################################
# Player routes:

app.add_url_rule(
    "/api/player-stats", "get_player_stats", get_player_stats, methods=["GET", "POST"]
)

app.add_url_rule(
    "/api/adv-player-stats",
    "get_adv_player_stats",
    get_adv_player_stats,
    methods=["GET", "POST"],
)

app.add_url_rule("/api/teams", "get_teams", get_teams, methods=["GET", "POST"])

app.add_url_rule(
    "/api/head-to-head", "get_h2h_stats", get_h2h_stats, methods=["GET", "POST"]
)
