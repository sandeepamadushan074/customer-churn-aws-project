-- Query 1: Count customers by churn status
SELECT
    Churn,
    COUNT(*) AS customer_count
FROM customer_churn_db.churn_data
GROUP BY Churn
ORDER BY customer_count DESC;


-- Query 2: Analyze churn by contract type
SELECT
    Contract,
    Churn,
    COUNT(*) AS customer_count
FROM customer_churn_db.churn_data
GROUP BY Contract, Churn
ORDER BY Contract, Churn;

-- Query 3: Calculate churn rate by contract type
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_churn_db.churn_data
GROUP BY Contract
ORDER BY churn_rate_percent DESC;

-- Query 4: Analyze churn by monthly charges
SELECT
    Churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(TRY_CAST(MonthlyCharges AS DOUBLE)), 2)
        AS average_monthly_charges,
    ROUND(AVG(TRY_CAST(tenure AS DOUBLE)), 2)
        AS average_tenure_months
FROM customer_churn_db.churn_data
GROUP BY Churn
ORDER BY Churn;

-- Query 5: Analyze churn by payment method
SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(
        CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM customer_churn_db.churn_data
GROUP BY PaymentMethod
ORDER BY churn_rate_percent DESC;