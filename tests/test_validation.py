import unittest
import pandas as pd
from src.data_cleaning import load_and_clean_data
from src.validation import validate_data, REQUIRED_COLUMNS


class TestValidation(unittest.TestCase):
    """Unit tests for the data validation rules."""

    @classmethod
    def setUpClass(cls):
        cls.clean_df = load_and_clean_data()

    def test_validate_clean_data_passes(self):
        """Verify that properly cleaned data has zero validation errors."""
        errors = validate_data(self.clean_df)
        self.assertEqual(len(errors), 0, f"Expected no validation errors, got: {errors}")

    def test_detect_missing_required_column(self):
        """Verify validation flags missing required columns."""
        for col in ["customerID", "Churn", "MonthlyCharges", "TotalCharges"]:
            with self.subTest(column=col):
                corrupted_df = self.clean_df.drop(columns=[col])
                errors = validate_data(corrupted_df)
                self.assertTrue(
                    any("Missing required columns" in err for err in errors),
                    f"Validation failed to detect missing column: {col}"
                )

    def test_detect_negative_tenure(self):
        """Verify validation catches negative tenure values."""
        corrupted_df = self.clean_df.copy()
        corrupted_df.loc[0, "tenure"] = -10
        errors = validate_data(corrupted_df)
        self.assertTrue(
            any("Negative tenure" in err for err in errors),
            "Validation should catch negative tenure."
        )

    def test_detect_negative_monthly_charges(self):
        """Verify validation catches negative MonthlyCharges."""
        corrupted_df = self.clean_df.copy()
        corrupted_df.loc[0, "MonthlyCharges"] = -50.0
        errors = validate_data(corrupted_df)
        self.assertTrue(
            any("Negative MonthlyCharges" in err for err in errors),
            "Validation should catch negative MonthlyCharges."
        )

    def test_detect_invalid_churn_category(self):
        """Verify validation catches non-binary Churn values."""
        corrupted_df = self.clean_df.copy()
        corrupted_df.loc[0, "Churn"] = "Unknown"
        errors = validate_data(corrupted_df)
        self.assertTrue(
            any("Invalid Churn categories" in err for err in errors),
            "Validation should catch invalid Churn categories."
        )


if __name__ == "__main__":
    unittest.main()
