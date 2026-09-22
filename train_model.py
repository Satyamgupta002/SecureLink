# train_model_persist.py

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# 1. Load data
# ============================================================

X = pd.read_csv(r'E:\Brave Downloads\SecureLink\data\x.csv')

y_raw = pd.read_csv(r'E:\Brave Downloads\SecureLink\data\y.csv')
y = y_raw["Label"]


# ============================================================
# 2. Remove accidentally saved index column
# ============================================================

if "Unnamed: 0" in X.columns:
    X = X.drop(columns=["Unnamed: 0"])


# ============================================================
# 3. Feature schema
# ============================================================

FEATURE_COLUMNS = [
    "URL length",
    "Number of dots",
    "Number of slashes",
    "Percentage of numerical characters",
    "Dangerous characters",
    "Dangerous TLD",
    "Entropy",
    "IP Address",
    "Domain name length",
    "Suspicious keywords",
    "Repetitions",
    "Redirections"
]


# Make sure training data has exactly these features
X = X[FEATURE_COLUMNS]


# ============================================================
# 4. Train-test split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=22,
    stratify=y
)


# ============================================================
# 5. Final Random Forest
# ============================================================

final_rf = RandomForestClassifier(
    n_estimators=344,
    max_depth=24,
    min_samples_split=5,
    min_samples_leaf=1,
    max_features="log2",
    class_weight="balanced",
    random_state=22,
    n_jobs=-1
)


# ============================================================
# 6. Train
# ============================================================

print("Training Random Forest...")

final_rf.fit(X_train, y_train)

print("Training completed.")


# ============================================================
# 7. Evaluate on test set
# ============================================================

y_pred = final_rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\nFinal Random Forest Results")
print("=" * 40)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1       : {f1:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 8. Save model + feature schema
# ============================================================

model_artifact = {
    "model": final_rf,
    "feature_columns": FEATURE_COLUMNS
}

joblib.dump(
    model_artifact,
    "phishing_model.pkl"
)

print("\nModel saved as phishing_model.pkl")