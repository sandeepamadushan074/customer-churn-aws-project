import pandas as pd


REQUIRED_COLUMNS = [
    "customerID",
    "Churn",
    "Contract",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]


def validate_data(df):
    """Validate required columns and basic data quality."""

    errors = []

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )

    if errors:
        return errors

    # Check duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        errors.append(
            f"Found {duplicate_count} duplicate rows."
        )

    # Check missing values
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        errors.append(
            f"Missing values found: {missing_values.to_dict()}"
        )

    # Check numeric columns
    for column in ["tenure", "MonthlyCharges", "TotalCharges"]:
        if not pd.api.types.is_numeric_dtype(df[column]):
            errors.append(
                f"{column} must contain numeric values."
            )

    # Check unusual values
    if (df["tenure"] < 0).any():
        errors.append("Negative tenure values found.")

    if (df["MonthlyCharges"] < 0).any():
        errors.append("Negative MonthlyCharges values found.")

    if not df["Churn"].isin(["Yes", "No"]).all():
        errors.append("Invalid Churn categories found.")

    return errors
if __name__ == "__main__":
    from src.data_cleaning import load_and_clean_data

    df = load_and_clean_data()
    errors = validate_data(df)

    if errors:
        print("\nValidation Errors:")
        for error in errors:
            print("-", error)
    else:
        print("\nValidation successful! No errors found.")