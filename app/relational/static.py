import pandas as pd
import requests
from bs4 import BeautifulSoup
from PandasBasketball import pandasbasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days

def _get_players_letter_dirs():
    """Returns list of URLs where each URL holds all the players
    with last names starting with each respective lettergraphene.Abstract()
    Example:
        ['http://www.basketball-reference.com/players/a/',
        'http://www.basketball-reference.com/players/b/',
        'http://www.basketball-reference.com/players/c/',
        'http://www.basketball-reference.com/players/d/',
        'http://www.basketball-reference.com/players/e/']
    """
    import string
    letters = string.ascii_lowercase
    players_letter_dirs = [f"http://www.basketball-reference.com/players/{letter}/" for letter in letters]
    return players_letter_dirs


def _get_players_tables():
    players_tables = []
    for letter_dir in _get_players_letter_dirs():
        r = requests.get(letter_dir)
        soup = BeautifulSoup(r.text, "html.parser")
        players_table = soup.find("table", id="players")
        players_tables.append(players_table)
    
    return players_tables

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

    for players_table in _get_players_tables():
        players_name_rows = players_table.find("tbody").find_all("th")
        filenames = [row["data-append-csv"] for row in players_name_rows]

        for row in players_name_rows:
            split_name = row.a.text.split()
            first = split_name[0]
            last = split_name[-1]
            encoding = row["data-append-csv"]
            player_dict[f"{first} {last}"] = encoding

    return player_dict   

def _get_full_player_urls():
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
    for letter_dir in _get_players_letter_dirs():
        for encoding in player_dict.values():
            if encoding.startswith(letter_dir[-2]):
                full_player_urls.append(letter_dir+encoding+".html")
    return full_player_urls

def create_player_stats_df(player_url, stat):
    return player_stats(requests.get(url), stat)

def create_all_player_stats_df(stat="per_minute"):
    player_stats_dfs = [create_player_stats_df(url, stat) for url in full_player_urls]
    all_player_stats_df = pd.concat(player_stats_dfs, keys=list(create_player_dict().keys())) # persist player_dict so don't have to call func each time
    return all_player_stats_df

def _reorder_cols(df,left: int=6, right: int=7):
    """Returns DataFrame with two columns reordered.  Enables `strip_left_cols()`. 
        Makes strippable columns are consecutive.

        Params:
        df: DataFrame to be reordered
        first: Int representing the original left index loc of the DF's list of cols
        second: Int representing the original right index loc of the DF's list of cols"""
    cols = list(df.columns)
    cols[left], cols[right] = cols[right], cols[left]
    return df[cols]

def _strip_left_cols(df, cols_to_strip):
    """Return passed DF with columns stripped columns equal to num_cols. 
        Used in merging so columns aren't duplicated and therefore renamed."""
    columnss = df.columns
    return df[columns[cols_to_strip:]]

def merge_player_dfs(basic_stats_df, adv_stats_df, cols_to_strip: int=7):

    return pd.merge(basic_stats_df, _strip_left_cols(adv_stats_df, cols_to_strip), left_index=True, right_index=True)