import pandas as pd
import requests
from bs4 import BeautifulSoup
from PandasBasketball import pandasbasketball as pb
from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days

def date_to_index(df, date_column='Date', inplace=True):
    """Replaces the index of target Pandas DataFrame with the desired column by label.
    Called when the index of the DF isn't already the desired date column."""
    if inplace:
        df = df.set_index(df[f"{date_column}"])
        return df
    else:
        return df.set_index(df[f"{date_column}"])

def reorder_cols(df,left=6, right=7):
    """Returns DataFrame with two columns reordered.  Enables `strip_left_cols()`. 
        Makes strippable columns are consecutive.

        Params:
        df: DataFrame to be reordered
        first: Int representing the original left index loc of the DF's list of cols
        second: Int representing the original right index loc of the DF's list of cols"""
    cols = list(df.columns)
    cols[left], cols[right] = cols[right], cols[left]
    return df[cols]

def strip_left_cols(df, cols_to_strip):
    """Return passed DF with columns stripped columns equal to num_cols. 
        Used in merging so columns aren't duplicated and therefore renamed."""
    columnss = df.columns
    return df[columns[cols_to_strip:]]

def merge_player_dfs(basic_stats_df, adv_stats_df, cols_to_strip=7):
    """Returns DataFrame with left passed DF inner joined with right passed DF 
        stripped of its non-numerical left cols
    """
    return pd.merge(basic_stats_df, _strip_left_cols(adv_stats_df, cols_to_strip), left_index=True, right_index=True)

def sampling(df, sample_rule):
    df.resample(rule=f"{sample_rule}")

def concat_row(row: pd.DataFrame, df: pd.DataFrame, to_top=True):
    """Returns a DataFrame that is a concatination of multiple DataFrames. 
        A DataFrame can be single row and likely will be.  DF/row are both assumed
        to be primed for concatenation already.  Other functions do the priming.

        Params:
        row: single row DataFrame to be appended to df
        df: DataFrame target for appended row
        to_top: bool determining whether the row is appanded to top of df or bottom
    """
    pd.concat([row,df], keys=list(PLAYER_DICT.keys())) # persist player_dict so don't have to call func each time