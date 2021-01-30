import pandas as pd
import requests
import string
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from PandasBasketball import pandasbasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days
import hashlib
import json
import time
from fuzzywuzzy import fuzz

PLAYER_BASE_URL = "https://www.basketball-reference.com/players/"
TEAM_BASE_URL = "https://www.basketball-reference.com/teams/"
PLAYER_REF_PATH = ""

def get_players_letter_dirs():
    """Returns list of URLs where each URL holds all the players
    with last names starting with each respective lettergraphene.Abstract()
    Example:
        ['http://www.basketball-reference.com/players/a/',
        'http://www.basketball-reference.com/players/b/',
        'http://www.basketball-reference.com/players/c/',
        'http://www.basketball-reference.com/players/d/',
        'http://www.basketball-reference.com/players/e/']
    """
    letters = string.ascii_lowercase
    players_letter_dirs = [f"http://www.basketball-reference.com/players/{letter}/" for letter in letters]
    return players_letter_dirs

def get_player_dict():
    f = open("/Users/samdillard/python/github.com/samhld/nba_stats/app/dbs/player_ref.json", "r")
    if f:
        player_dict = json.loads(f.read())
    else:
        from preprocessor.builders import create_player_dict
        player_dict = create_player_dict()
    return player_dict

def get_player_url(player):
    """Returns Str of full url for a player's stats page"""
    player_dict = get_player_dict()
    player_letter = player_dict[f"{player}"][0]
    return f"{PLAYER_BASE_URL}/{player_letter}/{player_dict[player]}.html"

def get_players_tables():
    players_tables = []
    for letter_dir in get_players_letter_dirs():
        r = requests.get(letter_dir)
        soup = BeautifulSoup(r.text, "html.parser")
        players_table = soup.find("table", id="players")
        players_tables.append(players_table)
    
    return players_tables

def get_full_player_urls(segment=slice(None)):
    """Returns list of URLs for all respective player pages
    Example:
    >> full_player_urls[400:1600:100]
    ['http://www.basketball-reference.com/players/b/bonnema01.html',
    'http://www.basketball-reference.com/players/b/brogaji01.html',
    'http://www.basketball-reference.com/players/b/burrobo01.html',
    'http://www.basketball-reference.com/players/c/catoke01.html',
    'http://www.basketball-reference.com/players/c/colliza01.html',
    'http://www.basketball-reference.com/players/c/cuetoal01.html',
    'http://www.basketball-reference.com/players/d/dawsoto01.html',
    'http://www.basketball-reference.com/players/d/doumbse01.html',
    'http://www.basketball-reference.com/players/e/ellinwa01.html',
    'http://www.basketball-reference.com/players/f/fesenky01.html',
    'http://www.basketball-reference.com/players/f/fundela01.html',
    'http://www.basketball-reference.com/players/g/gladnmi01.html']

    Params:
    segment: expects a slice
    """
    full_player_urls = []
    for letter_dir in get_players_letter_dirs():
        for encoding in list(get_player_dict().values())[segment]:
            if encoding.startswith(letter_dir[-2]):
                full_player_urls.append(letter_dir+encoding+".html")
    return full_player_urls

def hash_page(url):
    """
    Hashes a webpage.  Old hashes will be compared with new 
    hashes to monitor the existence of page changes.
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    return hashlib.md5(repr(soup).encode("utf-8"))

def compare_hash(hash1, hash2):
    """Return True if hashes are equal. Used for monitoring changes in webpages"""
    return hash1 == hash2


def match_player_names(input_name, player_dict):
    matches = []
    # if player_dict:
    for player in list(map(lambda player: player.lower(), player_dict.keys())):
        if fuzz.partial_ratio(input_name, player) > 75:
            matches.append(player)
    # else:
    #     # player_dict = get_player_dict()
    #     # for player in list(map(lambda player: player.lower(), player_dict.keys())):
    #     #     if fuzz.partial_ratio(input_name, player) > 75:
    #     #         matches.append(player)
    #     # print(player_dict)
    #     match_player_names(input_name, player_dict=get_player_dict())
    
    return matches
# def get_latest(table)

def _get_player_table(url, stat):
    
    one_header_tables = ["totals", "per_minute", "per_poss", "advanced",
                        "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                        "playoffs_per_poss", "playoffs_advanced"]
    
    two_header_tables = ["adj_shooting", "playoffs_shooting", "shooting", "pbp", "playoffs_pbp"]
    
    res = requests.get(url)
    
    if stat == "per_game":
        
        soup = bs(res.text, "lxml")
        table = soup.find("table", id="per_game")
        
    elif stat in one_header_tables or stat in two_header_tables:

        soup = bs(res.text, "lxml")
        comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and f'id="{stat}"' in x)
        soup = bs(comment_table, "lxml")
        table = soup.find("table", id=stat)
        
        if stat in two_header_tables:
            
            table.find("tr").decompose()

    else:
        raise TableNonExistent
    
    return table

def get_all_player_tables(url):
    
    supported_tables = ["totals", "per_minute", "per_poss", "advanced",
                        "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                        "playoffs_per_poss", "playoffs_advanced", "adj_shooting", 
                        "playoffs_shooting", "shooting", "pbp", "playoffs_pbp"]
    
    tables = []
    for table in supported_tables:
        print(table)
        tables.append(_get_player_table(url, table))
        
    return tables