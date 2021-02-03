from dataclasses import dataclass
import pandas as pd

@dataclass
class Player:
    name: str = ""
    encoding: str = ""
    urls: tuple=()
    active: bool=False  # most players are no longer active
    gamelog: pd.DataFrame = pd.DataFrame()
    per_game: pd.DataFrame = pd.DataFrame()
    per_36: pd.DataFrame = pd.DataFrame()
    per_poss: pd.DataFrame = pd.DataFrame()
    totals: pd.DataFrame = pd.DataFrame()
    advanced: pd.DataFrame = pd.DataFrame()
    playoffs_per_game: pd.DataFrame = pd.DataFrame()
    playoffs_per_36: pd.DataFrame = pd.DataFrame()
    playoffs_per_poss: pd.DataFrame = pd.DataFrame()
    playoffs_advanced: pd.DataFrame = pd.DataFrame()
    shooting: pd.DataFrame = pd.DataFrame()
    adj_shooting: pd.DataFrame = pd.DataFrame()
    playoffs_shooting: pd.DataFrame = pd.DataFrame()
    pbp: pd.DataFrame = pd.DataFrame()
    playoffs_pbp: pd.DataFrame = pd.DataFrame()





