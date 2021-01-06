import pandas as pd
from typing import List
from static import create_player_dict

PLAYER_DICT = create_player_dict()

def date_to_index(df, date_column='Date', inplace=True):
    """Replaces the index of target Pandas DataFrame with the desired column by label.
    Called when the index of the DF isn't already the desired date column."""
    if inplace:
        df = df.set_index(df[f"{date_column}"])
        return df
    else:
        return df.set_index(df[f"{date_column}"])

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