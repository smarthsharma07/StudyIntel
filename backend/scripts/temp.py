import pandas as pd

df = pd.read_csv("C:\\Users\\Smarth Sharma\\Desktop\\StudyIntel-1\\backend\\data\\processed\\studyintel_processed.csv")

corr = df.corr(numeric_only=True)

print(
    corr["productivity_rating"]
    .sort_values(ascending=False)
)