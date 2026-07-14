import pandas as pd


def load_csv(file):
    """
    Reads an uploaded CSV file into a DataFrame.
    """

    if file is None:
        return None

    return pd.read_csv(file)