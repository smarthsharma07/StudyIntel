from pathlib import Path

import pandas as pd


def load_study_logs(file_path: str | Path) -> pd.DataFrame:
    print(f"Loading file: {file_path}")

    try:
        df = pd.read_csv(file_path)

        print("Loaded successfully!")
        print(df.shape)

        return df

    except FileNotFoundError:
        print("File not found!")
        return pd.DataFrame()

