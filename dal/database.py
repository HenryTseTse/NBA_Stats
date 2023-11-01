from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from models import db, User, PlayerStats

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode("UTF-8")


def signup(username, password, first_name, last_name):
    """Sign up user.
    Hashes password and adds user to system.
    """
    hashed_pwd = hash_password(password)

    user = User(
        username=username,
        password=hashed_pwd,
        first_name=first_name,
        last_name=last_name,
    )

    db.session.add(user)
    return user


def get_leader_stats():
    all_leaders = PlayerStats.query.all()
    scoring_leaders = []
    rebounding_leaders = []
    assisting_leaders = []
    stealing_leaders = []
    blocking_leaders = []

    for player in all_leaders:
        if player.title == "pts":
            scoring_leaders.append(player)
        elif player.title == "reb":
            rebounding_leaders.append(player)
        elif player.title == "ast":
            assisting_leaders.append(player)
        elif player.title == "stl":
            stealing_leaders.append(player)
        else:
            blocking_leaders.append(player)

    result = {
        "scoring_leaders": scoring_leaders,
        "rebounding_leaders": rebounding_leaders,
        "assisting_leaders": assisting_leaders,
        "stealing_leaders": stealing_leaders,
        "blocking_leaders": blocking_leaders,
    }

    return result
