Create Athena database and table

CREATE DATABASE IF NOT EXISTS customer_churn_db;

CREATE EXTERNAL TABLE IF NOT EXISTS customer_churn_db.churn_data (
    customerID STRING,
    gender STRING,
    SeniorCitizen INT,
    Partner STRING,
    Dependents STRING,
    tenure DOUBLE,
    PhoneService STRING,
    MultipleLines STRING,
    InternetService STRING,
    OnlineSecurity STRING,
    OnlineBackup STRING,
    DeviceProtection STRING,
    TechSupport STRING,
    StreamingTV STRING,
    StreamingMovies STRING,
    Contract STRING,
    PaperlessBilling STRING,
    PaymentMethod STRING,
    MonthlyCharges STRING,
    TotalCharges DOUBLE,
    Churn STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"'
)
STORED AS TEXTFILE
LOCATION 's3://customer-churn-student-2026-susl/processed/'
TBLPROPERTIES ('skip.header.line.count'='1');
