import pandas as pd

from utils.schema_mapper import map_columns


def load_csv(file, dataset_type):
    """
    Reads a CSV file and standardizes
    its columns using AI.
    """

    if file is None:
        return None

    try:

        df = pd.read_csv(file)

        df = map_columns(
            df,
            dataset_type
        )

        return df

    except Exception as e:

        raise ValueError(
            f"Error processing {dataset_type} CSV:\n{e}"
        )