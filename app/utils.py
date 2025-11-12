import pandas as pd
from pathlib import Path


def load_country_data(country_name: str):
    """Load cleaned country CSV independent of current working directory.

    Looks for the CSV in the repository-level `data/` directory where this
    project lives. Returns a DataFrame if found, otherwise returns None.
    """
    repo_root = Path(__file__).resolve().parents[1]
    file_name = f"{country_name.lower().replace(' ', '')}_clean.csv"
    file_path = repo_root / "data" / file_name

    if file_path.exists():
        return pd.read_csv(file_path)
    return None
