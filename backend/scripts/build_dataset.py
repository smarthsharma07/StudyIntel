
from src.data.loader import load_study_logs
from src.features.feature_engineering import engineer_features
from src.preprocessing import preprocessing

RAW_DATA = r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1\backend\data\raw\study_logs.csv"
PROCESSED_DATA = r"C:\Users\Smarth Sharma\Desktop\StudyIntel-1\backend\data\processed\studyintel_processed.csv"


def build_dataset():

    df = load_study_logs(RAW_DATA)

    df = engineer_features(df)

    df,encoders = preprocessing.preprocess_data(df)
    print(type(df))
    print(df)
    df.to_csv(PROCESSED_DATA, index=False)

    print(f"Saved processed dataset to {PROCESSED_DATA}")


if __name__ == "__main__":
    build_dataset()