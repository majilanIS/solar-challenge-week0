import pandas as pd
from pathlib import Path


def load_country_data(country_name: str):
    """Load cleaned country CSV independent of current working directory.

    Looks for the CSV in the repository-level `data/` directory where this
    project lives. Returns a DataFrame if found, otherwise returns None.
    """
    # Resolve repository root (two levels up from this file: repo_root/ app/ utils.py -> repo_root)
    repo_root = Path(__file__).resolve().parents[1]
    file_name = f"{country_name.lower().replace(' ', '')}_clean.csv"
    file_path = repo_root / "data" / file_name

    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception:
            # If reading fails return None to let the caller handle the error/UI
            return None
    # Fallback: try to find a relevant raw CSV in the repository `raw/` directory
    raw_dir = repo_root / "raw"
    if raw_dir.exists():
        # Try a few sensible patterns based on the country name
        country_token = country_name.lower().replace(' ', '')
        candidates = list(raw_dir.glob(f"*{country_token}*.csv"))
        # also try the first word (e.g., 'sierraleone' -> 'sierraleone' or 'sierra')
        first_token = country_name.lower().split()[0]
        candidates += [p for p in raw_dir.glob(f"*{first_token}*.csv") if p not in candidates]

        for p in candidates:
            try:
                print(f"Trying raw file fallback: {p}")
                return pd.read_csv(p)
            except Exception:
                continue

    return None
