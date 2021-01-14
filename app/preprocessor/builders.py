import pandas as pd
import requests
from bs4 import BeautifulSoup
# from mungers import 
from PandasBasketball import pandasbasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days
from scraper.getters import get_players_tables


class Table:
    def __init__(self, url=None):
        self.request = requests.get(url)
        self.soup = BeautifulSoup(self.request, "html.parser")


def create_player_dict():
    """Returns dictionary mapping full player names to their page encoding determined by B-R
    Sample:
        {'Alaa Abdelnaby': 'abdelal01',
        'Zaid Abdul-Aziz': 'abdulza01',
        'Kareem Abdul-Jabbar': 'abdulka01',
        'Mahmoud Abdul-Rauf': 'abdulma02',
        'Tariq Abdul-Wahad': 'abdulta01',
        'Shareef Abdur-Rahim': 'abdursh01'}
    """
    player_dict = {}

    for players_table in get_players_tables():
        players_name_rows = players_table.find("tbody").find_all("th")
        filenames = [row["data-append-csv"] for row in players_name_rows]

        for row in players_name_rows:
            split_name = row.a.text.split()
            first = split_name[0]
            last = split_name[-1]
            encoding = row["data-append-csv"]
            player_dict[f"{first} {last}"] = encoding

    return player_dict 

"""
Below functions are shortcuts to creating DataFrames.
They will likely be used to initially generate DataFrames in cases of failure / data loss.
"""
def create_player_stats_df(player_url, stat):
    return player_stats(requests.get(url), stat)

def create_all_player_stats_df(stat="per_minute"):
    player_stats_dfs = [create_player_stats_df(url, stat) for url in full_player_urls]
    all_player_stats_df = pd.concat(player_stats_dfs, keys=list(create_player_dict().keys())) # persist player_dict so don't have to call func each time
    return all_player_stats_df

def get_last_row(table):
    body = table.find("tbody")
    rows = body.find_all("tr")
    return rows[-1]