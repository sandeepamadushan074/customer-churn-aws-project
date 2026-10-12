
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Telco-Customer-Churn.csv"


def load_and_clean_data():
    """Load the original dataset and perform basic cleaning."""

    df = pd.read_csv(DATA_PATH)

    print("Original Dataset Shape:", df.shape)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows without a customer ID
    if "customerID" in df.columns:
        df = df.dropna(subset=["customerID"])

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"], errors="coerce"
    )
    df["TotalCharges"] = df["TotalCharges"].fillna(
        df["MonthlyCharges"] * df["tenure"]
    )
    # Create TenureGroup feature
    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=[
            "0-12 Months",
            "13-24 Months",
            "25-48 Months",
            "49-72 Months"
        ]
    )

    print("Cleaned Dataset Shape:", df.shape)
    print("\nMissing Values:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    return df


if __name__ == "__main__":
    cleaned_df = load_and_clean_data()

    output_path = BASE_DIR / "outputs" / "cleaned_customer_churn.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)
