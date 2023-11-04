"""User model tests."""

# run these tests like:
#
#    python -m unittest test_player_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import PlayerStats, db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ["DATABASE_URL"] = "postgresql:///nba-users-tests"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class PlayerModelTestCase(TestCase):
    """Test models for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        p1 = PlayerStats(
            season=2012,
            first_name="Player",
            last_name="One",
            pts=20,
            reb=5,
            ast=5,
            stl=5,
            blk=5,
            rank=1,
            title="pts",
            image="/static/images/default.jpg",
        )
        pid1 = 666
        p1.id = pid1

        p2 = PlayerStats(
            season=2012,
            first_name="Player",
            last_name="Two",
            pts=19,
            reb=5,
            ast=5,
            stl=5,
            blk=5,
            rank=1,
            title="pts",
            image="/static/images/default.jpg",
        )
        pid2 = 777
        p2.id = pid2

        db.session.commit()

        p1 = PlayerStats.query.get(pid1)
        p2 = PlayerStats.query.get(pid2)

        self.p1 = p1
        self.pid1 = pid1

        self.p2 = p2
        self.pid2 = pid2

        self.client = app.test_client()

    def tearDown(self) -> None:
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_repr_method(self):
        """Test repr method for users"""
        p3 = PlayerStats(
            season=2012,
            first_name="Player",
            last_name="Three",
            pts=18,
            reb=5,
            ast=5,
            stl=5,
            blk=5,
            rank=3,
            title="pts",
            image="/static/images/default.jpg",
        )

        db.session.add(p3)
        db.session.commit()

        expected_repr = f"<PlayerStats {p3.id} {p3.season} {p3.first_name} {p3.last_name} {p3.pts} {p3.reb} {p3.ast} {p3.stl} {p3.blk} {p3.title} {p3.rank}>"
        self.assertEqual(repr(p3), expected_repr)
