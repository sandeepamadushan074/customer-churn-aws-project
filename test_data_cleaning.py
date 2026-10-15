import unittest
import pandas as pd
from pathlib import Path
from src.data_cleaning import load_and_clean_data, DATA_PATH


class TestDataCleaning(unittest.TestCase):
    """Unit tests for the data cleaning pipeline."""

    @classmethod
    def setUpClass(cls):
        cls.df = load_and_clean_data()

    def test_dataset_exists(self):
        """Verify the raw dataset file exists at DATA_PATH."""
        self.assertTrue(DATA_PATH.exists(), f"Dataset file not found at {DATA_PATH}")

    def test_cleaned_dataset_not_empty(self):
        """Verify cleaned dataset contains records."""
        self.assertGreater(self.df.shape[0], 0, "Cleaned dataset should contain rows.")
        self.assertGreater(self.df.shape[1], 0, "Cleaned dataset should contain columns.")

    def test_tenure_group_feature_created(self):
        """Verify the TenureGroup feature is created with expected categories."""
        self.assertIn("TenureGroup", self.df.columns, "TenureGroup feature must be present.")
        expected_categories = {"0-12 Months", "13-24 Months", "25-48 Months", "49-72 Months"}
        actual_categories = set(self.df["TenureGroup"].dropna().unique())
        self.assertTrue(
            actual_categories.issubset(expected_categories),
            f"Unexpected categories found in TenureGroup: {actual_categories}"
        )

    def test_no_duplicate_rows(self):
        """Verify that duplicate rows are completely removed."""
        duplicate_count = self.df.duplicated().sum()
        self.assertEqual(duplicate_count, 0, "Cleaned dataset must not have duplicate rows.")

    def test_total_charges_numeric_and_no_nulls(self):
        """Verify TotalCharges is converted to numeric and contains no nulls."""
        self.assertTrue(
            pd.api.types.is_numeric_dtype(self.df["TotalCharges"]),
            "TotalCharges must be numeric."
        )
        self.assertEqual(
            self.df["TotalCharges"].isnull().sum(),
            0,
            "TotalCharges should have 0 null values after imputation."
        )


if __name__ == "__main__":
    unittest.main()
