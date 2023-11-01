"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py

import os
from unittest import TestCase
from basketball_app.models import db
from basketball_app.functions import *

os.environ['DATABASE_URL'] = "postgresql:///nba-users-tests"

from basketball_app.app import app

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = signup("username", "password", "test", "user")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = signup("username1", "password", "test", "one")
        self.u1_id = 666
        self.u1.id = self.u1_id
        self.u2 = signup("username2", "password", "test", "two")
        self.u2_id = 777
        self.u2.id = self.u2_id

        db.session.commit()
        

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_get_anon_user(self):
        with self.client as c:
            resp = c.get("/")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Current Scoring Leaders", str(resp.data))
            self.assertIn("Current Rebound Leaders", str(resp.data))
            self.assertIn("Current Assist Leaders", str(resp.data))
            self.assertIn("Current Steal Leaders", str(resp.data))
            self.assertIn("Current Block Leaders", str(resp.data))
    
    def test_get_teams(self):
        with self.client as c:
            resp = c.get("/api/teams")

            self.assertEquals(resp.status_code, 200)
            
            self.assertIn("NBA Teams", str(resp.data))
            self.assertIn("West Teams", str(resp.data))
            self.assertIn("East Team", str(resp.data))

    def test_get_h2h(self):
        with self.client as c:
            resp = c.get("/api/head-to-head")

            self.assertEquals(resp.status_code, 200)

            self.assertIn("Head-to-Head", str(resp.data))

    def test_get_player_stats_form(self):
        with self.client as c:
            resp = c.get("/api/player-stats")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Player Career Search", str(resp.data))

    def test_get_advanced_search(self):
        with self.client as c:
            resp = c.get("/api/adv-player-stats")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Advanced Player Search", str(resp.data))

    def test_get_h2h_form_valid(self):
        with self.client as c:
            resp = c.post("/api/head-to-head", data={"team": 14, "season": 2012, "postseason":"false"})

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Team Stats", str(resp.data))

    def test_get_h2h_form_invalid(self):
        with self.client as c:
            resp = c.post("/api/head-to-head", data={"team": 14, "season": 19, "postseason":"false"})

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Year must be between 1946-Current", str(resp.data))

    def test_get_player_stats_form_valid(self):
        with self.client as c:
            resp = c.post("/api/player-stats", data={"first_name": "kobe", "last_name": "bryant"})

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Career Average Stats for Kobe Bryant", str(resp.data))
    
    def test_get_player_stats_form_invalid(self):
        with self.client as c:
            resp = c.post("/api/player-stats", data={"first_name": "not", "last_name": "aname"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Player not found", str(resp.data))
    

    def test_get_advanced_stats_form(self):
        with self.client as c:
            resp = c.post("/api/adv-player-stats", data={"first_name": "kobe", "last_name": "bryant", "start_date":"2001-1-12","end_date":"2014-4-13","pts":50,
                                                         "ast":5,"reb":5})
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Advanced Stats for Kobe Bryant", str(resp.data))

    def test_get_advanced_stats_form_invalid_format(self):
        with self.client as c:
            resp = c.post("/api/adv-player-stats", data={"first_name": "kobe", "last_name": "bryant", "start_date":"1-12-2001","end_date":"4-13-2014","pts":50,
                                                     "ast":5,"reb":5}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Wrong Input Format!", str(resp.data))
    
    def test_get_advanced_stats_form_invalid_name(self):
        with self.client as c:
            resp = c.post("/api/adv-player-stats", data={"first_name": "not", "last_name": "aname", "start_date":"2001-1-12","end_date":"2014-4-13","pts":50,
                                                     "ast":5,"reb":5}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Player not found", str(resp.data))