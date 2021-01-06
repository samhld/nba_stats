
def date_to_index(df, date_column='Date', inplace=True):
    """Replaces the index of target Pandas DataFrame with the desired column by label.
    Called when the index of the DF isn't already the desired date column."""
    if inplace:
        df = df.set_index(df[f"{date_column}"])
        return df
    else:
        return df.set_index(df[f"{date_column}"])