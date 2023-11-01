"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from basketball_app.models import User, db
from basketball_app.functions import *
from basketball_app.dal.database import signup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///nba-users-tests"


# Now we can import app

from basketball_app.app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test models for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = signup("test1", "password", "test", "one")
        uid1 = 666
        u1.id = uid1

        u2 = signup("test2", "password", "test", "two")
        uid2 = 777
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self) -> None:
        res = super().tearDown()
        db.session.rollback()
        return res
    
    
    def test_repr_method(self):
        """Test repr method for users"""
        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            first_name="test",
            last_name="user"
        )

        db.session.add(u)
        db.session.commit()

        expected_repr = f"<User {u.id} {u.username} {u.first_name} {u.last_name}>"
        self.assertEqual(repr(u), expected_repr)
    
    
    def test_signup(self):
        """Signing up a user"""
        u = signup("username", "password", "test", "one")
        uid = 9999
        u.id = uid
        db.session.commit()

        u = User.query.get(uid)

        self.assertIsNotNone(u)
        self.assertEqual(u.username, "username")
        self.assertNotEqual(u.password, "password")
        self.assertEqual(u.first_name, "test")
        self.assertEqual(u.last_name, "one")

        #Bcrypt strings start with $2b$
        self.assertTrue(u.password.startswith("$2b$"))
    
    def test_invalid_username(self):
        """Invalid Username"""
        u = signup(None, "password", "test", "one")
        uid = 9999
        u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        
    def test_invalid_password(self):
        """Invalid Password""" 
        with self.assertRaises(ValueError) as context:
            signup("test", None, "test", "one")

        with self.assertRaises(ValueError) as context:
            signup("test", None, "test", "one")
    
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("notmyusername", "password"))
    
    def test_invalid_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "notmypassword"))
