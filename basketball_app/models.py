from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        u = self
        return f"<User {u.id} {u.username} {u.first_name} {u.last_name}>"

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class PlayerStats(db.Model):
    __tablename__ = "playerstats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    season = db.Column(db.Integer)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    pts = db.Column(db.Float)
    reb = db.Column(db.Float)
    ast = db.Column(db.Float)
    stl = db.Column(db.Float)
    blk = db.Column(db.Float)
    title = db.Column(db.Text)
    rank = db.Column(db.Integer)

    def __repr__(self):
        p = self
        return f"<PlayerStats {p.id} {p.season} {p.first_name} {p.last_name} {p.pts} {p.reb} {p.ast} {p.stl} {p.blk} {p.title} {p.rank}>"


# Extra Database Model
# class PlayerIDs(db.Model):

#     __tablename__ = 'playerids'
#     id = db.Column(db.Integer,
#                 primary_key=True,
#                 autoincrement=True)
#     name = db.Column(db.Text,
#             nullable=False)
#     player_id = db.Column(db.Integer,
#             nullable=False)

#     def __repr__(self):
#         p = self
#         return f"<PlayerId {p.id} {p.name} {p.player_id}>"
