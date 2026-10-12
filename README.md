
# AWS Customer Churn Prediction Project

## 1. Project Overview

This project analyzes customer churn in a telecommunications dataset and demonstrates an AWS-based data processing pipeline.

Customer churn occurs when a customer stops using a company's service. Understanding churn patterns helps businesses identify customer groups that may need better services and retention strategies.

This group project includes:

- AWS cloud storage and data processing.
- Data validation and cleaning.
- Exploratory Data Analysis (EDA).
- Machine learning model development and evaluation.
- SQL analytics using Amazon Athena.
- Business insights and recommendations.
- GitHub collaboration and project documentation.

## 2. Dataset

**Dataset:** Telco Customer Churn  
**Original file:** `Telco-Customer-Churn.csv`  
**Original dataset size:** 7,043 customer records  
**Target column:** `Churn`

The dataset contains customer information such as:

- Customer demographics.
- Contract type.
- Customer tenure.
- Monthly and total charges.
- Payment method.
- Services used.
- Customer churn status.

The original CSV is uploaded to the Amazon S3 `raw/` folder. The processed dataset is saved to the S3 `processed/` folder.

The team should use the agreed processed dataset for EDA, machine learning, and SQL analysis to maintain consistency.

## 3. Project Structure

The target repository structure is:

```text
customer-churn-aws-project/
├── data/
│   └── Telco-Customer-Churn.csv
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   ├── data_cleaning.py
│   ├── data_pipeline.py
│   ├── validation.py
│   ├── logging_config.py
│   ├── train_logistic_regression.py
│   └── train_random_forest.py
├── sql/
│   ├── analysis_queries.sql
│   ├── create_table.sql
│   └── query_results/
│       ├── query_01_results.csv
│       ├── query_02_results.csv
│       ├── query_03_results.csv
│       ├── query_04_results.csv
│       └── query_05_results.csv
├── outputs/
│   ├── figures/
│   ├── model_metrics.csv
│   └── feature_importance.csv
├── docs/
│   ├── aws_architecture.png
│   ├── business_recommendations.md
│   ├── technical_report.pdf
│   └── demo_evidence/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

This structure describes the expected project organization. All listed files should be verified in the repository before final submission.

## 4. Technologies Used

- Python
- pandas and NumPy
- Matplotlib and Seaborn
- scikit-learn
- Google Colab
- Amazon S3
- AWS Lambda
- Amazon CloudWatch
- Amazon Athena
- Git and GitHub

## 5. AWS Data Pipeline

The project uses Amazon S3 and AWS Lambda to process the customer churn dataset.

The intended workflow is:

1. Upload the original CSV file to the S3 `raw/` folder.
2. An S3 Object Created event triggers the configured Lambda function.
3. Lambda reads the uploaded CSV file.
4. The dataset is validated and cleaned.
5. The processed CSV is saved to the S3 `processed/` folder.
6. CloudWatch Logs are used to inspect execution messages and errors.
7. The agreed processed dataset is used for EDA, machine learning, and SQL analysis.
8. Important outputs and screenshots are stored in the GitHub repository.

The S3 event notification should monitor only the intended raw CSV files. This helps avoid repeatedly triggering Lambda when it writes the processed output.

The pipeline should also be tested with repeated uploads to verify how the fixed output filename behaves.

## 6. Data Validation and Cleaning

The data processing stage checks the dataset before analysis.

The validation and cleaning process should consider:

- Required columns.
- Missing values.
- Duplicate records.
- Incorrect data types.
- Invalid numeric values.
- Consistent column names and output formats.

The Lambda cleaning process and notebook preprocessing should follow agreed rules. Any differences, such as missing-value handling, duplicate removal, or data type conversion, should be documented.

The processed dataset should be checked for consistent row counts and column names before being used by other team members.

## 7. Exploratory Data Analysis (EDA)

Student 2 is responsible for EDA using `notebooks/01_eda.ipynb`.

The analysis includes:

1. Overall customer churn distribution.
2. Churn by contract type.
3. Monthly charges by churn status.
4. Customer tenure by churn status.

The notebook should be run from beginning to end using the agreed processed dataset. Charts should be saved in `outputs/figures/`, and the main findings should be documented using the actual results.

## 8. Machine Learning and Model Evaluation

Student 3 is responsible for developing and evaluating Logistic Regression and Random Forest models.

The models should use a consistent dataset split and appropriate evaluation methods.

### Random Forest Evaluation

The recorded Random Forest evaluation results are:

| Metric | Result |
|---|---:|
| Accuracy | 0.7587 |
| Precision | 0.5310 |
| Recall | 0.7781 |
| F1-score | 0.6312 |
| Cross-validation F1-score | 0.6362 |

The recorded classification threshold is 0.50.

The recorded confusion matrix is:

```text
[[778, 257],
 [ 83, 291]]
```

The recorded important Random Forest features include:

- Tenure.
- Month-to-month contract.
- TotalCharges.
- MonthlyCharges.

The exact feature importance values should be taken from the generated model output.

### Logistic Regression Evaluation

The Logistic Regression model must also be evaluated using the actual model output.

Its accuracy, precision, recall, F1-score, and other required metrics should be documented from the generated evaluation results. Values should not be estimated or invented.

The team should verify that both model evaluations use the agreed dataset and document any differences in preprocessing.

## 9. SQL Analytics Using Amazon Athena

Student 4 is responsible for SQL analytics, business insights, and integration.

The SQL analysis uses Amazon Athena with the database and table:

- Database: `customer_churn_db`
- Table: `customer_churn_db.churn_data`

The SQL scripts are stored in `sql/`:

- `analysis_queries.sql`
- `create_table.sql`

The results of the five SQL queries are stored in `sql/query_results/`.

### 9.1 Overall Customer Churn

| Churn status | Number of customers |
|---|---:|
| No | 5,174 |
| Yes | 1,869 |
| Total | 7,043 |

The overall churn rate is approximately **26.5%**.

### 9.2 Churn by Contract Type

| Contract | Total customers | Churned customers | Churn rate |
|---|---:|---:|---:|
| Month-to-month | 3,875 | 1,655 | 42.71% |
| One year | 1,473 | 166 | 11.27% |
| Two year | 1,695 | 48 | 2.83% |

Month-to-month customers have the highest churn rate in this analysis.

### 9.3 Average Monthly Charges and Tenure

| Churn status | Average monthly charges | Average tenure (months) |
|---|---:|---:|
| No | 61.27 | 37.57 |
| Yes | 74.44 | 17.98 |

Customers who churned had higher average monthly charges and lower average tenure than customers who did not churn.

### 9.4 Churn by Payment Method

| Payment method | Total customers | Churned customers | Churn rate |
|---|---:|---:|---:|
| Electronic check | 2,365 | 1,071 | 45.29% |
| Mailed check | 1,612 | 308 | 19.11% |
| Bank transfer (automatic) | 1,544 | 258 | 16.71% |
| Credit card (automatic) | 1,522 | 232 | 15.24% |

Electronic check users have the highest churn rate among the payment methods in this analysis.

These SQL results are descriptive findings. They show associations in the dataset and do not prove that a particular contract, payment method, or monthly charge directly causes churn.

## 10. Business Recommendations

Based on the SQL analysis, the following actions are recommended.

### 10.1 Encourage Long-Term Contracts

Month-to-month customers have a churn rate of 42.71%, compared with 11.27% for one-year contracts and 2.83% for two-year contracts.

**Recommendation:** Test suitable discounts, benefits, or retention offers that encourage month-to-month customers to consider longer-term contracts. Monitor the results to determine whether the offers improve customer retention.

### 10.2 Review the Payment Experience

Electronic check users have a churn rate of 45.29%, higher than the rates for the other payment methods.

**Recommendation:** Investigate whether customers experience difficulties with the electronic check payment process. Explain convenient payment alternatives, including automatic payments, and monitor whether customer retention improves.

### 10.3 Improve the Early Customer Experience

Customers who churned have an average tenure of 17.98 months, compared with 37.57 months for customers who did not churn. Their average monthly charges are also higher.

**Recommendation:** Provide early support to new customers, explain plan charges clearly, and review whether customers are receiving suitable plans for their needs. Contact customers who show signs of dissatisfaction and evaluate whether these actions reduce churn.

More details are available in `docs/business_recommendations.md`.

## 11. Setup Instructions

### Prerequisites

- Python installed on the computer.
- GitHub access to the project repository.
- Access to the required AWS resources for cloud processing and SQL analysis.
- The project dataset and required Python packages.

### Install Dependencies

Clone or download the repository, open a terminal in the project root, and run:

```bash
pip install -r requirements.txt
```

### Run the EDA Notebook

1. Open `notebooks/01_eda.ipynb` in Google Colab or a compatible Jupyter environment.
2. Provide the agreed dataset at the path expected by the notebook.
3. Run all notebook cells from beginning to end.
4. Check the generated charts and results.

### Run the AWS Pipeline

1. Upload the original CSV to the configured S3 `raw/` folder.
2. Confirm that the S3 event notification is configured correctly.
3. Check the Lambda execution result.
4. Inspect CloudWatch Logs for errors or processing messages.
5. Verify that the processed CSV was created in the S3 `processed/` folder.

### Run SQL Analysis

1. Open Amazon Athena in the configured AWS region.
2. Select the `customer_churn_db` database.
3. Run the queries in `sql/analysis_queries.sql`.
4. Compare the results with the saved CSV files in `sql/query_results/`.

The table creation script is included for documentation and reproducibility. Do not recreate an existing table unnecessarily.

## 12. Testing and Verification

The following checks are required before final submission:

- Test data validation and cleaning functions.
- Run the EDA notebook from beginning to end.
- Reproduce both machine learning model evaluations.
- Execute all five SQL queries.
- Verify that row counts and metrics are consistent.
- Upload a new CSV through the AWS pipeline.
- Test repeated uploads and fixed-filename output behaviour.
- Inspect CloudWatch Logs.
- Save relevant screenshots and evidence in `docs/demo_evidence/`.

These checks should be marked as completed only after the corresponding tests have actually been performed.

## 13. Security and Cost Considerations

### Security

- Never commit AWS access keys, secret keys, passwords, or private credentials to GitHub.
- Use appropriate IAM permissions for Lambda and other AWS resources.
- Use an IAM execution role for Lambda instead of hardcoding AWS credentials.
- Review `.gitignore` before committing files.
- Do not commit the `.venv/` directory or other unnecessary local environment files.

### Cost

- Monitor AWS usage and charges through the billing dashboard.
- Avoid unnecessary Lambda invocations.
- Keep CloudWatch Logs and S3 storage within appropriate limits.
- Run Athena queries only when required.
- Remove unused resources after testing when appropriate.

## 14. Limitations

- The results depend on the quality and coverage of the available dataset.
- The analysis identifies associations, not proven causes of customer churn.
- Machine learning performance depends on data preprocessing, feature selection, and evaluation methods.
- The pipeline must be tested with new and repeated uploads to confirm reliable behaviour.
- Reported metrics must be reproducible using the saved code and agreed dataset.

## 15. Team Contributions

- **Student 1:** AWS Cloud and Data Pipeline.
- **Student 2:** Data Cleaning and Exploratory Data Analysis.
- **Student 3:** Machine Learning and Model Evaluation.
- **Student 4:** SQL Analytics, Business Insights, and Integration.

Each student should contribute their source code, results, and documentation to the shared repository.

## 16. Project Deliverables

The final repository should include:

- Original dataset and agreed data processing code.
- EDA notebook and generated figures.
- Both machine learning scripts and evaluation results.
- SQL scripts and query result CSV files.
- AWS architecture diagram.
- Technical report and demo evidence.
- Business recommendations.
- Tests, dependency requirements, and setup instructions.
- This README file.

Before submission, the team should verify that all required files exist and that the documented workflow and results match the actual project.
