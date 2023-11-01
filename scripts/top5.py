"""Retrieve Top 5 players in each category and store every player into database"""
import time

import requests
from requests.exceptions import HTTPError

from app import app
from dal.database import connect_db
from models import db, PlayerStats
from readcsv import get_player_image

BASE_URL = "https://www.balldontlie.io/api/v1"
DEFAULT_IMAGE = "/static/images/default.jpg"


def update_database(top5_list):
    """Update playerstats database"""
    for player in top5_list:
        image = get_player_image(player["first_name"], player["last_name"])
        if image:
            player_stat = PlayerStats(
                season=player["season"],
                first_name=player["first_name"],
                last_name=player["last_name"],
                pts=player["pts"],
                reb=player["reb"],
                ast=player["ast"],
                stl=player["stl"],
                blk=player["blk"],
                rank=player["rank"],
                title=player["title"],
                image=image,
            )
        else:
            player_stat = PlayerStats(
                season=player["season"],
                first_name=player["first_name"],
                last_name=player["last_name"],
                pts=player["pts"],
                reb=player["reb"],
                ast=player["ast"],
                stl=player["stl"],
                blk=player["blk"],
                rank=player["rank"],
                title=player["title"],
                image=DEFAULT_IMAGE,
            )
        db.session.add(player_stat)
        db.session.commit()


def top5_list_sort(cat, input_list):
    """Sort and Rank Top 5 in each category"""
    input_list = sorted(input_list, key=lambda i: i[cat], reverse=True)
    rk = 1
    for item in input_list:
        item["title"] = cat
        item["rank"] = rk
        rk += 1
    return input_list


def decide_top5_players(
    top5_list, cat_stat, category, first_name, last_name, player_data
):
    """Compare Stats to current Top 5"""
    if len(top5_list) < 5:
        top5_list.append(
            {
                "season": player_data["season"],
                "first_name": first_name,
                "last_name": last_name,
                "pts": player_data["pts"],
                "reb": player_data["reb"],
                "ast": player_data["ast"],
                "stl": player_data["stl"],
                "blk": player_data["blk"],
            }
        )

    else:
        if cat_stat > top5_list[-1][category]:
            top5_list.pop()
            top5_list.append(
                {
                    "season": player_data["season"],
                    "first_name": first_name,
                    "last_name": last_name,
                    "pts": player_data["pts"],
                    "reb": player_data["reb"],
                    "ast": player_data["ast"],
                    "stl": player_data["stl"],
                    "blk": player_data["blk"],
                }
            )
            print(">>>top5 list updated", category, flush=True)
    top5_list = top5_list_sort(category, top5_list, first_name, last_name)
    return top5_list


def parse_stat_by_category(
    category, cat_stat, first_name, last_name, player_data, top5_guys
):
    """Determine Top 5"""
    if category == "pts":
        top5_guys.top5_scorers = decide_top5_players(
            top5_guys.top5_scorers,
            cat_stat,
            category,
            first_name,
            last_name,
            player_data,
        )
    elif category == "reb":
        top5_guys.top5_rebounders = decide_top5_players(
            top5_guys.top5_rebounders,
            cat_stat,
            category,
            first_name,
            last_name,
            player_data,
        )
    elif category == "ast":
        top5_guys.top5_assisters = decide_top5_players(
            top5_guys.top5_assisters,
            cat_stat,
            category,
            first_name,
            last_name,
            player_data,
        )
    elif category == "stl":
        top5_guys.top5_stealers = decide_top5_players(
            top5_guys.top5_stealers,
            cat_stat,
            category,
            first_name,
            last_name,
            player_data,
        )
    else:
        top5_guys.top5_blockers = decide_top5_players(
            top5_guys.top5_blockers,
            cat_stat,
            category,
            first_name,
            last_name,
            player_data,
        )

    return top5_guys


def get_top5_category_players(id, first_name, last_name, top5_guys):
    """Retrieve Top 5"""
    search_player_stat_URL = f"{BASE_URL}/season_averages"
    query = {"player_ids[]": id}

    response = make_requests(search_player_stat_URL, query)
    player_data = response["data"]
    print(">>>player id", id, "name", first_name, " ", last_name, flush=True)

    if player_data:
        category = ["pts", "reb", "ast", "stl", "blk"]
        for cat in category:
            top5_guys = parse_stat_by_category(
                cat,
                player_data[0][cat],
                first_name,
                last_name,
                player_data[0],
                top5_guys,
            )

    return top5_guys


def make_requests(url, query):
    """Make API Requests"""
    timer.tik = sleep_timer(timer.tik)
    timer.tik += 1
    try:
        response = requests.get(url, params=query)
        return response.json()
    except:
        print("Too many requests to API!", flush=True)
        time.sleep(60)
        return requests.get(url, params=query).json()


def sleep_timer(i):
    """60 second timer for every 50 requests"""
    while i > 44:
        time.sleep(70)
        i = 0
    return i


class Timer:
    def __init__(self, tik):
        self.tik = tik


timer = Timer(0)


class Top5:
    """Class for Top 5"""

    def __init__(
        self,
        top5_scorers,
        top5_rebounders,
        top5_assisters,
        top5_stealers,
        top5_blockers,
    ):
        self.top5_scorers = top5_scorers
        self.top5_rebounders = top5_rebounders
        self.top5_assisters = top5_assisters
        self.top5_stealers = top5_stealers
        self.top5_blockers = top5_blockers


top5_guys = Top5([], [], [], [], [])

search_players_URL = f"{BASE_URL}/players"
query = {"per_page": 100}
response = make_requests(search_players_URL, query)
data = response["data"]
total_pages = response["meta"]["total_pages"]
if data:
    for page in range(28, total_pages + 1):
        query = {"page": page, "per_page": 100}
        page_response = make_requests(search_players_URL, query)
        all_players = page_response["data"]
        if all_players:
            for player in all_players:
                id = player.get("id", 0)
                first_name = player.get("first_name", "NULL")
                last_name = player.get("last_name", "NULL")
                top5_guys = get_top5_category_players(
                    id, first_name, last_name, top5_guys
                )

db.drop_all()
db.create_all()
update_database(top5_guys.top5_scorers)
update_database(top5_guys.top5_rebounders)
update_database(top5_guys.top5_assisters)
update_database(top5_guys.top5_stealers)
update_database(top5_guys.top5_blockers)
