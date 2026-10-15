from pathlib import Path
import pandas as pd

import unittest

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Telco-Customer-Churn.csv"


class TestDataset(unittest.TestCase):
    """Basic checks for raw dataset loading and structure."""

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(DATA_PATH)

    def test_raw_dataset_shape(self):
        """Verify the raw dataset has 7043 rows and 21 columns."""
        self.assertEqual(self.df.shape, (7043, 21))

    def test_churn_column_present(self):
        """Verify the target Churn column is present."""
        self.assertIn("Churn", self.df.columns)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    print(df.head())
    print("Dataset shape:", df.shape)
    print(df["Churn"].value_counts())
    print("Columns:", df.columns.tolist())
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nChurn count:")
    print(df["Churn"].value_counts())
    print("\nChurn percentage:")
    print(df["Churn"].value_counts(normalize=True) * 100)