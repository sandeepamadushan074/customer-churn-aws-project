import pandas as pd

df = pd.read_csv("../data/Telco-Customer-Churn.csv")

print(df.head())
print("Dataset shape:", df.shape)
print(df["Churn"].value_counts())
print("Columns:", df.columns.tolist())

print("Missing values:")
print(df.isnull().sum())

print("\nChurn count:")
print(df["Churn"].value_counts())

print("\nChurn percentage:")
print(df["Churn"].value_counts(normalize=True) * 100)