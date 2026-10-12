
import boto3
import pandas as pd

from io import StringIO
from urllib.parse import unquote_plus

from src.validation import validate_data
from src.logging_config import logger


S3_BUCKET = "customer-churn-student-2026-susl"


def process_s3_file(bucket, key):
    """Read, clean, validate, and save a CSV file from S3."""

    s3 = boto3.client("s3")

    logger.info("Started processing file: %s", key)

    try:
        # Read CSV from S3
        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        df = pd.read_csv(response["Body"])

        logger.info("Original dataset shape: %s", df.shape)

        # Check required columns before cleaning
        required_columns = [
            "customerID",
            "Churn",
            "Contract",
            "tenure",
            "MonthlyCharges",
            "TotalCharges"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            logger.error(
                "Missing required columns: %s",
                missing_columns
            )
            return

        # Remove unnecessary spaces from text columns
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].str.strip()

        # Convert numeric columns to the correct data types
        for column in [
            "tenure",
            "MonthlyCharges",
            "TotalCharges"
        ]:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

        # Remove rows without essential values
        df = df.dropna(
            subset=["customerID", "Churn"]
        ).copy()

        # Handle missing TotalCharges values
        missing_total = df["TotalCharges"].isna()

        df.loc[missing_total, "TotalCharges"] = (
            df.loc[missing_total, "MonthlyCharges"]
            * df.loc[missing_total, "tenure"]
        )

        # Remove duplicate rows
        duplicate_count = df.duplicated().sum()
        df = df.drop_duplicates().copy()

        logger.info(
            "Removed %s duplicate rows",
            duplicate_count
        )

        # Validate the cleaned dataset
        errors = validate_data(df)

        if errors:
            logger.error(
                "Validation failed for %s: %s",
                key,
                errors
            )
            return

        logger.info("Validation successful")
        logger.info("Cleaned dataset shape: %s", df.shape)

        # Convert cleaned dataset to CSV format
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Save output in the S3 processed/ folder
        filename = key.split("/")[-1]
        output_key = f"processed/cleaned_{filename}"

        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        logger.info(
            "Cleaned file saved to s3://%s/%s",
            bucket,
            output_key
        )

    except Exception:
        logger.exception(
            "Failed to process file: %s",
            key
        )
        raise


def lambda_handler(event, context):
    """AWS Lambda entry point for new CSV uploads."""

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]

        key = unquote_plus(
            record["s3"]["object"]["key"]
        )

        # Process only CSV files in raw/
        if key.startswith("raw/") and key.lower().endswith(".csv"):
            process_s3_file(bucket, key)
        else:
            logger.info("Skipping file: %s", key)

    return {
        "statusCode": 200,
        "body": "Processing completed"
    }
