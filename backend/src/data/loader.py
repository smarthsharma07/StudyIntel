from pathlib import Path

import pandas as pd


def load_study_logs(file_path: str | Path) -> pd.DataFrame:

    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        return pd.DataFrame()

    except Exception as e:
        print(f"Error loading study logs: {e}")
        return pd.DataFrame()