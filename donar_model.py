import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# -------------------- LOAD DATA --------------------
df = pd.read_csv("data/transfusion.csv")

# -------------------- RENAME COLUMNS --------------------
df.rename(columns={
    "Recency (months)": "Recency",
    "Frequency (times)": "Frequency",
    "Monetary (c.c. blood)": "Monetary",
    "Time (months)": "Time",
    "whether he/she donated blood in March 2007": "target"
}, inplace=True)

# -------------------- FEATURES & TARGET --------------------
X = df[["Recency", "Frequency", "Monetary", "Time"]]
y = df["target"]

# -------------------- TRAIN TEST SPLIT --------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------- MODEL --------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train, y_train)

# -------------------- PREDICTION --------------------
preds = model.predict(X_test)

# -------------------- EVALUATION --------------------
print("Accuracy:", accuracy_score(y_test, preds))
print("\nClassification Report:\n", classification_report(y_test, preds))

# -------------------- SAVE MODEL --------------------
joblib.dump(model, "donor_model.pkl")

print("\n✅ Donor model saved successfully!")