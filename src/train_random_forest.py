import pandas as pd
from pathlib import Path
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score
)

from src.data_cleaning import load_and_clean_data


# Set output paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# Load dataset
df = load_and_clean_data()

X = df.drop(
    columns=["customerID", "Churn", "gender"],
    errors="ignore"
)
y = df["Churn"].map({"No": 0, "Yes": 1})

if y.isna().any():
    raise ValueError("Churn contains missing or unexpected values.")


# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)


# Identify column types
categorical_cols = X_train.select_dtypes(
    include=["object", "category", "str"]
).columns.tolist()

numerical_cols = X_train.select_dtypes(
    include=["number"]
).columns.tolist()


# Prepare preprocessing steps
numerical_transformer = SimpleImputer(strategy="median")

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)


# Build Random Forest pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(random_state=42))
    ]
)


# Set hyperparameter options
param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__max_depth": [None, 10, 20, 30],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 4],
    "model__max_features": ["sqrt", "log2"],
    "model__class_weight": [None, "balanced", "balanced_subsample"]
}


# Find the best model
random_search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_grid,
    n_iter=20,
    scoring="f1",
    cv=5,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

print("\nTraining Random Forest model...")
random_search.fit(X_train, y_train)

best_model = random_search.best_estimator_

print("\nBest Parameters:")
print(random_search.best_params_)

print("\nBest Cross-Validation F1-score:")
print(round(random_search.best_score_, 4))


# Predict churn probabilities
y_prob = best_model.predict_proba(X_test)[:, 1]


# Compare prediction thresholds
thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
threshold_results = []

for threshold in thresholds:
    temp_pred = (y_prob >= threshold).astype(int)

    threshold_results.append({
        "Threshold": threshold,
        "Precision": precision_score(
            y_test, temp_pred, zero_division=0
        ),
        "Recall": recall_score(
            y_test, temp_pred, zero_division=0
        ),
        "F1-score": f1_score(
            y_test, temp_pred, zero_division=0
        )
    })

threshold_df = pd.DataFrame(threshold_results)
best_result = threshold_df.loc[threshold_df["F1-score"].idxmax()]
best_threshold = float(best_result["Threshold"])

print("\nThreshold Comparison:")
print(threshold_df.to_string(index=False))
print("\nSelected Threshold:", best_threshold)


# Evaluate the final model
y_pred = (y_prob >= best_threshold).astype(int)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("\n===== Random Forest Results =====")
print(f"Accuracy: {accuracy:.4f}")
print(f"Churn Precision: {precision:.4f}")
print(f"Churn Recall: {recall:.4f}")
print(f"Churn F1-score: {f1:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1],
    target_names=["No", "Yes"],
    zero_division=0
))


# Create and save confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

print("\nConfusion Matrix:")
print(cm)

fig, ax = plt.subplots(figsize=(7, 5))

ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["No Churn", "Churn"]
).plot(
    ax=ax,
    cmap="Blues",
    values_format="d"
)

ax.set_title("Random Forest - Confusion Matrix")
fig.tight_layout()

confusion_matrix_path = (
    FIGURES_DIR / "random_forest_confusion_matrix.png"
)

fig.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

print("\nConfusion matrix saved:", confusion_matrix_path)


# Save evaluation results
metrics_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Churn Precision",
        "Churn Recall",
        "Churn F1-score",
        "Best Cross-Validation F1-score",
        "Selected Threshold"
    ],
    "Score": [
        accuracy,
        precision,
        recall,
        f1,
        random_search.best_score_,
        best_threshold
    ]
})

metrics_df.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)
threshold_df.to_csv(
    OUTPUT_DIR / "threshold_comparison.csv",
    index=False
)


# Calculate feature importance
feature_names = best_model.named_steps[
    "preprocessor"
].get_feature_names_out()

importance_values = best_model.named_steps[
    "model"
].feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_values
}).sort_values(by="Importance", ascending=False)

print("\nTop 15 Important Features:")
print(importance_df.head(15).to_string(index=False))

importance_df.to_csv(
    OUTPUT_DIR / "feature_importance.csv",
    index=False
)


# Save trained model
joblib.dump(
    {
        "model": best_model,
        "threshold": best_threshold
    },
    OUTPUT_DIR / "customer_churn_random_forest.joblib"
)

print("\nRandom Forest training completed.")
print("Output Folder:", OUTPUT_DIR)
