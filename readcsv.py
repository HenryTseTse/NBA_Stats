import pandas as pd
import requests
from collections import ChainMap

IMAGE_URL = (
    "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190"
)


df = pd.read_csv(
    "../static/NBA_Player_IDs.csv",
    encoding="unicode_escape",
    usecols=["BBRefName", "NBAID"],
).dropna()
result = df.to_dict(orient="split")["data"]
dict_list = [{k.lower(): int(v)} for k, v in result]
my_dict = dict(ChainMap(*dict_list))


def get_player_image(first_name, last_name):
    full_name = str(first_name) + " " + str(last_name)
    player_id = my_dict.get(full_name.lower(), "none")
    URL = f"{IMAGE_URL}/{player_id}.png"
    # for data in df.itertuples():
    #     temp_name = str(data[1])
    #     if temp_name.lower() == full_name.lower():
    #         player_id = int(data[7])
    #         break
    # URL = f"{IMAGE_URL}/{player_id}.png"
    try:
        session = requests.Session()
        response = session.head(URL)
        if response.headers["Content-Type"] != "image/png":
            print(first_name, " ", last_name, " has no image!")
            return None
        else:
            print("Find image for ", first_name, " ", last_name)
            return URL
    except:
        print("get_player_image error")
        return None
