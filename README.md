
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
- AWS-based customer churn prediction using a trained Random Forest model.
- An API endpoint for submitting customer details and receiving predictions.

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

This structure describes the expected project organization. All listed files should be verified in the repository before final submission. The deployed model and AWS configuration are also maintained in AWS.

## 4. Technologies Used

- Python
- pandas and NumPy
- Matplotlib and Seaborn
- scikit-learn
- Google Colab
- Amazon S3
- AWS Lambda
- Amazon API Gateway
- Amazon CloudWatch
- Amazon Athena
- AWS IAM
- Git and GitHub

## 5. AWS Data Pipeline and Prediction Service

The project uses Amazon S3 and AWS Lambda to process customer data and generate churn predictions. Amazon API Gateway provides an HTTP endpoint for prediction requests, while Amazon CloudWatch supports monitoring and troubleshooting.

### 5.1 AWS Resources

| AWS Resource | Configuration |
|---|---|
| AWS Region | `eu-north-1` |
| S3 Bucket | `customer-churn-student-2026-susl` |
| Lambda Function | `customer-churn-predictor` |
| API Gateway | `customer-churn-predictor-API` |
| Trained Random Forest model | `outputs/customer_churn_random_forest.joblib` |

### 5.2 Data Processing Workflow

The original data-processing workflow is intended to use Amazon S3 and AWS Lambda.

1. Upload the original CSV file to the S3 `raw/` folder.
2. An S3 Object Created event triggers the configured Lambda function.
3. Lambda reads the uploaded CSV file.
4. The dataset is validated and cleaned.
5. The processed CSV is saved to the S3 `processed/` folder.
6. CloudWatch Logs are used to inspect execution messages and errors.
7. The agreed processed dataset is used for EDA, machine learning, and SQL analysis.
8. Important outputs and screenshots are stored in the GitHub repository.

The raw-to-processed workflow must be configured and verified separately from the prediction workflow described below. The S3 event notification should monitor only the intended input files to avoid repeated invocations when Lambda writes output files.

### 5.3 S3 Batch Prediction Workflow

The deployed prediction service supports batch predictions from customer CSV files.

1. Upload a customer CSV file to the S3 `incoming/` folder.
2. The configured S3 Object Created event triggers the `customer-churn-predictor` Lambda function for CSV uploads.
3. Lambda reads the uploaded CSV file.
4. Lambda loads the trained Random Forest model from S3.
5. The model predicts customer churn for the input records.
6. Lambda saves the prediction results as a CSV file under `outputs/predictions/`.
7. CloudWatch Logs can be inspected for execution messages and errors.

**Example input:**

`incoming/customer_churn_test_data.csv`

**Example output:**

`outputs/predictions/customer_churn_test_data_predictions.csv`

The batch prediction workflow has been tested successfully, and a prediction CSV was generated in the S3 output folder.

The output filename is based on the input filename, with `_predictions.csv` appended before the file extension.

Repeated uploads and fixed-filename output behaviour should be tested to ensure the pipeline behaves as expected.

### 5.4 API-Based Prediction Workflow

Amazon API Gateway exposes the Lambda prediction function through an HTTP endpoint.

The workflow is:

1. A client sends customer details as a JSON POST request.
2. API Gateway forwards the request to the `customer-churn-predictor` Lambda function.
3. Lambda processes the customer details and loads the trained model from S3 when required.
4. The model predicts the customer's churn status.
5. Lambda returns the prediction result as JSON.

**API Endpoint:**

`https://ueu30rw8tl.execute-api.eu-north-1.amazonaws.com/default/customer-churn-predictor`

**HTTP Method:** `POST`

**Content-Type:** `application/json`

The API endpoint was tested successfully using PowerShell.

Example response from a successful test:

```json
{
  "churn_prediction": "No",
  "churn_probability": 0.4026,
  "threshold": 0.5
}
```

This result represents one particular test request. The model predicted `No` because the churn probability was below the classification threshold of `0.5`.

The prediction is an estimate based on the trained model and does not guarantee the customer's future behaviour.

### 5.5 Monitoring and Permissions

- AWS Lambda uses an IAM execution role to access the required AWS resources.
- Amazon CloudWatch Logs provides Lambda execution logs for monitoring and troubleshooting.
- The S3 event notification must be configured for the intended input files.
- API Gateway must have permission to invoke the Lambda function.
- S3 permissions must allow the function to read the model and input files and write prediction outputs.

The configured IAM permissions should follow the principle of least privilege.

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

The prediction Lambda function also expects the input CSV or JSON fields to match the format required by the deployed model.

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

### 8.1 Random Forest Evaluation

The recorded Random Forest evaluation results are:

| Metric | Result |
|---|---:|
| Accuracy | 0.7587 |
| Precision | 0.5310 |
| Recall | 0.7781 |
| F1-score | 0.6312 |
| Cross-validation F1-score | 0.6362 |

The recorded classification threshold is `0.50`.

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

The recorded metrics should be reproduced using the saved training code and agreed dataset before final submission.

### 8.2 Logistic Regression Evaluation

The Logistic Regression model must also be evaluated using the actual model output.

Its accuracy, precision, recall, F1-score, and other required metrics should be documented from the generated evaluation results. Values should not be estimated or invented.

The team should verify that both model evaluations use the agreed dataset and document any differences in preprocessing.

### 8.3 Model Deployment and Prediction

The trained Random Forest model is stored in Amazon S3 and used by AWS Lambda for customer churn prediction.

The deployed model expects the feature columns used during model training. The input data must follow the same preprocessing and feature-format requirements.

The Lambda prediction logic derives the `TenureGroup` feature from `tenure` using these ranges:

- `0-12 Months`
- `13-24 Months`
- `25-48 Months`
- `49-72 Months`

The `customerID`, `Churn`, and `gender` columns are not model input features for this deployed Random Forest model.

The prediction service returns:

- `churn_prediction`: the predicted churn class.
- `churn_probability`: the estimated churn probability.
- `threshold`: the classification threshold used by the prediction logic.

The deployed model and its preprocessing requirements must remain consistent with the model used during training.

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

### Run the AWS Batch Prediction Pipeline

1. Open Amazon S3 in the `eu-north-1` region.
2. Upload a valid customer CSV file to `incoming/` in the `customer-churn-student-2026-susl` bucket.
3. Confirm that the S3 event notification is configured for the intended CSV files.
4. Check the `customer-churn-predictor` Lambda execution.
5. Inspect CloudWatch Logs if troubleshooting is required.
6. Verify that the prediction CSV was created under `outputs/predictions/`.

### Test the Prediction API

The API can be tested using PowerShell.

Set the endpoint:

```powershell
$uri = "https://ueu30rw8tl.execute-api.eu-north-1.amazonaws.com/default/customer-churn-predictor"
```

Prepare customer details:

```powershell
$body = @{
    SeniorCitizen = 0
    Partner = "Yes"
    Dependents = "No"
    tenure = 12
    PhoneService = "Yes"
    MultipleLines = "No"
    InternetService = "DSL"
    OnlineSecurity = "No"
    OnlineBackup = "Yes"
    DeviceProtection = "No"
    TechSupport = "No"
    StreamingTV = "No"
    StreamingMovies = "No"
    Contract = "Month-to-month"
    PaperlessBilling = "Yes"
    PaymentMethod = "Electronic check"
    MonthlyCharges = 70.5
    TotalCharges = 850.0
} | ConvertTo-Json
```

Send the POST request:

```powershell
try {
    $response = Invoke-RestMethod `
        -Uri $uri `
        -Method POST `
        -ContentType "application/json" `
        -Body $body

    Write-Host "`nAPI Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 5
}
catch {
    Write-Host "`nHTTP Request Failed:" -ForegroundColor Red

    if ($_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message
    }
    else {
        Write-Host $_.Exception.Message
    }
}
```

A successful response contains the prediction class, churn probability, and classification threshold. The result may differ when different customer details are submitted.

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
- Upload a new CSV through the AWS batch prediction pipeline.
- Verify that the prediction CSV is generated in S3.
- Test repeated uploads and fixed-filename output behaviour.
- Test the API with valid customer details.
- Test API error handling with invalid input.
- Inspect CloudWatch Logs.
- Save relevant screenshots and evidence in `docs/demo_evidence/`.

The S3 batch prediction workflow and API prediction endpoint have been tested successfully.

Other checks should be marked as completed only after the corresponding tests have actually been performed.

## 13. Security and Cost Considerations

### Security

- Never commit AWS access keys, secret keys, passwords, or private credentials to GitHub.
- Use appropriate IAM permissions for Lambda and other AWS resources.
- Use an IAM execution role for Lambda instead of hardcoding AWS credentials.
- Review `.gitignore` before committing files.
- Do not commit the `.venv/` directory or other unnecessary local environment files.
- Restrict access to S3 input files, model files, and prediction outputs to authorized users.
- Ensure that API Gateway has permission to invoke the intended Lambda function.
- Avoid exposing sensitive customer information in public repositories or logs.

### Cost

- Monitor AWS usage and charges through the billing dashboard.
- Avoid unnecessary Lambda invocations.
- Keep CloudWatch Logs and S3 storage within appropriate limits.
- Run Athena queries only when required.
- Remove unused resources after testing when appropriate.
- Review the costs of AWS services before extending the project.

## 14. Limitations

- The results depend on the quality and coverage of the available dataset.
- The analysis identifies associations, not proven causes of customer churn.
- Machine learning performance depends on data preprocessing, feature selection, and evaluation methods.
- The deployed prediction model requires input features in the expected format.
- The prediction probability is a model estimate, not a guarantee of future customer behaviour.
- The batch pipeline must be tested with new and repeated uploads to confirm reliable behaviour.
- The API should be tested with invalid and incomplete input to verify error handling.
- Reported metrics must be reproducible using the saved code and agreed dataset.
- The original raw-to-processed data pipeline and the deployed prediction pipeline have different S3 prefixes and should be documented and verified separately.

## 15. Team Contributions

- **Sandeepa:** AWS Cloud and Data Pipeline.
- **Pasindi:** Data Cleaning and Exploratory Data Analysis.
- **Avindu:** Machine Learning and Model Evaluation.
- **Uvindu 4:** SQL Analytics, Business Insights, and Integration.

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
- Documentation for the S3 batch prediction workflow.
- Documentation and test evidence for the API prediction endpoint.
- This README file.

Before submission, the team should verify that all required files exist and that the documented workflow and results match the actual project.
