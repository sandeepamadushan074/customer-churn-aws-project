
# AWS Customer Churn Prediction Project

## 1. Project Overview

This project analyzes customer churn in a telecommunications dataset and demonstrates an AWS-based data processing pipeline.

Customer churn means that a customer stops using a company's service. Understanding churn can help businesses identify customer groups that may need better service or retention strategies.

This group project includes:
- AWS cloud storage and data processing.
- Data validation and cleaning.
- Exploratory Data Analysis (EDA).
- Machine learning model development and evaluation.
- SQL analytics and business recommendations.

## 2. Dataset

Dataset: Telco Customer Churn

File name: `Telco-Customer-Churn.csv`

The dataset contains customer information such as contract type, tenure, monthly charges, services, and churn status.

The original dataset is uploaded to the AWS S3 `raw/` folder.

## 3. Project Structure

```text
AWS Project/
├── data/
│   └── Telco-Customer-Churn.csv
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── data_pipeline.py
│   ├── validation.py
│   ├── logging_config.py
│   ├── train_logistic_regression.py
│   └── train_random_forest.py
├── outputs/
│   ├── figures/
│   ├── model_metrics.csv
│   └── other generated results
├── docs/
│   └── aws_architecture.png
├── tests/
│   └── test_dataset.py
├── .gitignore
├── requirements.txt
└── README.md
```

Some files may be added as the project develops.

## 4. Technologies Used

- Python
- pandas and NumPy
- Matplotlib and Seaborn
- scikit-learn
- Google Colab
- Amazon S3
- AWS Lambda
- Amazon CloudWatch
- Git and GitHub

## 5. AWS Data Pipeline

The AWS pipeline uses Amazon S3 to store the original and processed datasets.

1. Upload the original CSV file to the S3 `raw/` folder.
2. An S3 Object Created event triggers the configured AWS Lambda function.
3. Lambda reads the CSV file and performs data processing.
4. The cleaned dataset is saved to the S3 `processed/` folder.
5. Lambda execution messages and errors can be checked in Amazon CloudWatch Logs.

The S3 trigger should only monitor `raw/` CSV files to avoid repeatedly processing output files.

## 6. Data Validation and Cleaning

The pipeline checks:
- Required columns.
- Missing values.
- Duplicate rows.
- Incorrect data types.
- Invalid numeric values.

Cleaning rules should be applied consistently so that the processed dataset can be used for EDA and machine learning.

## 7. Exploratory Data Analysis

Student 2 performs EDA using Google Colab.

The analysis includes:
1. Overall customer churn distribution.
2. Churn by contract type.
3. Monthly charges by churn status.
4. Customer tenure by churn status.

Charts and findings should be saved in the project outputs and explained using the actual results.

## 8. Local Setup

Python dependencies can be installed from the project root:

```bash
pip install -r requirements.txt
```

The EDA notebook is designed to run in Google Colab. Upload the notebook and provide the dataset before running its cells.

## 9. GitHub Collaboration and Security

GitHub is used to store the project source code, notebooks, documentation, and selected output files.

- Do not commit AWS access keys, secret keys, passwords, or private credentials.
- Do not commit the `.venv/` folder.
- Review `.gitignore` before pushing files.
- Give team members repository access through GitHub repository settings.
- Use an AWS IAM role for Lambda permissions rather than hardcoding AWS credentials.

## 10. Limitations

- The results depend on the dataset's quality and coverage.
- EDA findings must be based on the generated charts and actual data.
- A successful Lambda test does not automatically prove every new CSV file is processed correctly.
- Machine learning performance must be evaluated using appropriate test data.

## 11. Team Contributions

- Student 1: AWS Cloud and Data Pipeline.
- Student 2: Data Cleaning and Exploratory Data Analysis.
- Student 3: Machine Learning and Model Evaluation.
- Student 4: SQL Analytics, Business Insights and Integration.
