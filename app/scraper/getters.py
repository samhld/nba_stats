import pandas as pd
import requests
import string
from bs4 import BeautifulSoup
from PandasBasketball import pandasbasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days
import hashlib

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


def get_players_tables():
    players_tables = []
    for letter_dir in get_players_letter_dirs():
        r = requests.get(letter_dir)
        soup = BeautifulSoup(r.text, "html.parser")
        players_table = soup.find("table", id="players")
        players_tables.append(players_table)
    
    return players_tables

def get_full_player_urls():
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
    """
    full_player_urls = []
    for letter_dir in get_players_letter_dirs():
        for encoding in player_dict.values():
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



# def get_latest(table)